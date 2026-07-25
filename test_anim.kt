import androidx.compose.foundation.lazy.LazyItemScope
import androidx.compose.ui.Modifier
import androidx.compose.foundation.ExperimentalFoundationApi

@OptIn(ExperimentalFoundationApi::class)
fun LazyItemScope.test(mod: Modifier): Modifier {
    return mod.animateItemPlacement()
}
