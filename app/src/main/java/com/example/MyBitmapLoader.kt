package com.example

import android.content.Context
import android.graphics.Bitmap
import android.net.Uri
import androidx.media3.common.util.BitmapLoader
import com.google.common.util.concurrent.ListenableFuture
import com.google.common.util.concurrent.SettableFuture
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import coil.imageLoader
import coil.request.ImageRequest
import coil.request.videoFrameMillis

class MyBitmapLoader(val context: Context) : BitmapLoader {
    override fun supportsMimeType(mimeType: String) = true
    override fun decodeBitmap(data: ByteArray): ListenableFuture<Bitmap> {
        val future = SettableFuture.create<Bitmap>()
        val bmp = android.graphics.BitmapFactory.decodeByteArray(data, 0, data.size)
        if (bmp != null) future.set(bmp) else future.setException(Exception("err"))
        return future
    }
    override fun loadBitmap(uri: Uri): ListenableFuture<Bitmap> {
        val future = SettableFuture.create<Bitmap>()
        CoroutineScope(Dispatchers.IO).launch {
            try {
                // 1. Try Coil image loading (covers image files and supported media)
                try {
                    val req = ImageRequest.Builder(context).data(uri).size(512).build()
                    val result = context.imageLoader.execute(req)
                    val dr = result.drawable
                    if (dr is android.graphics.drawable.BitmapDrawable) {
                        future.set(dr.bitmap)
                        return@launch
                    }
                } catch (e: Exception) {}

                // 2. Try MediaMetadataRetriever (embedded artwork or video frame)
                val retriever = android.media.MediaMetadataRetriever()
                try {
                    retriever.setDataSource(context, uri)
                    val pic = retriever.embeddedPicture
                    if (pic != null) {
                        val bmp = android.graphics.BitmapFactory.decodeByteArray(pic, 0, pic.size)
                        if (bmp != null) {
                            future.set(bmp)
                            return@launch
                        }
                    }
                    val frame = if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O_MR1) {
                        retriever.getScaledFrameAtTime(1000000L, android.media.MediaMetadataRetriever.OPTION_CLOSEST_SYNC, 512, 512)
                            ?: retriever.frameAtTime
                    } else {
                        retriever.frameAtTime
                    }
                    if (frame != null) {
                        future.set(frame)
                        return@launch
                    }
                } catch (e: Exception) {
                } finally {
                    try { retriever.release() } catch (e: Exception) {}
                }

                // 3. Try ContentResolver loadThumbnail on Android 10+
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.Q) {
                    try {
                        val thumb = context.contentResolver.loadThumbnail(uri, android.util.Size(512, 512), null)
                        if (thumb != null) {
                            future.set(thumb)
                            return@launch
                        }
                    } catch (e: Exception) {}
                }

                future.setException(Exception("No bitmap available for $uri"))
            } catch(e: Exception) { 
                future.setException(e) 
            }
        }
        return future
    }
}
