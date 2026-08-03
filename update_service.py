import re

with open("app/src/main/java/com/example/service/CompressionService.kt", "r") as f:
    content = f.read()

old_process = """    private suspend fun processImages(uris: List<String>, maxWidth: Int, maxHeight: Int) {"""
new_process = """    private suspend fun processImages(uris: List<String>, maxWidth: Int, maxHeight: Int, quality: Int, formatStr: String) {"""
content = content.replace(old_process, new_process)

old_start = """        val maxWidth = intent.getIntExtra("maxWidth", -1)
        val maxHeight = intent.getIntExtra("maxHeight", -1)"""
new_start = """        val maxWidth = intent.getIntExtra("maxWidth", -1)
        val maxHeight = intent.getIntExtra("maxHeight", -1)
        val quality = intent.getIntExtra("quality", 80)
        val formatStr = intent.getStringExtra("format") ?: "JPEG\""""
content = content.replace(old_start, new_start)

old_launch = """            processImages(uris, maxWidth, maxHeight)"""
new_launch = """            processImages(uris, maxWidth, maxHeight, quality, formatStr)"""
content = content.replace(old_launch, new_launch)

old_logic = """                    if (maxWidth > 0 && maxHeight > 0) {
                        val ratio = kotlin.math.min(maxWidth.toFloat() / bitmap.width, maxHeight.toFloat() / bitmap.height)
                        if (ratio < 1f) {
                            val newW = (bitmap.width * ratio).toInt()
                            val newH = (bitmap.height * ratio).toInt()
                            outBitmap = Bitmap.createScaledBitmap(bitmap, newW, newH, true)
                        }
                    }
                    val origName = getOriginalFileName(uri)
                    val fileName = "${origName}_compressed.jpg"
                    val outStream: OutputStream? = getOutputStream(outputUriStr, fileName)
                    if (outStream != null) {
                        outBitmap.compress(Bitmap.CompressFormat.JPEG, 80, outStream)
                        outStream.close()
                    }"""

new_logic = """                    if (maxWidth > 0 && maxHeight > 0) {
                        val maxDim = maxOf(maxWidth, maxHeight).toFloat()
                        val minDim = minOf(maxWidth, maxHeight).toFloat()
                        
                        val targetW = if (bitmap.width > bitmap.height) maxDim else minDim
                        val targetH = if (bitmap.width > bitmap.height) minDim else maxDim
                        
                        val ratio = minOf(targetW / bitmap.width, targetH / bitmap.height)
                        
                        if (ratio < 1f) {
                            val newW = (bitmap.width * ratio).toInt()
                            val newH = (bitmap.height * ratio).toInt()
                            outBitmap = Bitmap.createScaledBitmap(bitmap, newW, newH, true)
                        }
                    }
                    
                    val compressFormat = when (formatStr) {
                        "PNG" -> Bitmap.CompressFormat.PNG
                        "WEBP" -> if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) Bitmap.CompressFormat.WEBP_LOSSY else Bitmap.CompressFormat.WEBP
                        else -> Bitmap.CompressFormat.JPEG
                    }
                    val ext = formatStr.lowercase()
                    
                    val origName = getOriginalFileName(uri)
                    val fileName = "${origName}_compressed.${ext}"
                    val outStream: OutputStream? = getOutputStream(outputUriStr, fileName, ext)
                    if (outStream != null) {
                        outBitmap.compress(compressFormat, quality, outStream)
                        outStream.close()
                    }"""
content = content.replace(old_logic, new_logic)

old_out = """    private fun getOutputStream(outputUriStr: String?, fileName: String): OutputStream? {"""
new_out = """    private fun getOutputStream(outputUriStr: String?, fileName: String, ext: String): OutputStream? {"""
content = content.replace(old_out, new_out)

content = content.replace("\"image/jpeg\"", "\"image/${ext}\"")

with open("app/src/main/java/com/example/service/CompressionService.kt", "w") as f:
    f.write(content)
