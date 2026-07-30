import androidx.compose.ui.layout.layout
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.Constraints

fun test() {
    val rotateConfig = 90
    Modifier.layout { measurable, constraints ->
        if (rotateConfig == 90 || rotateConfig == 270) {
            val swappedConstraints = Constraints(
                minWidth = constraints.minHeight,
                maxWidth = if (constraints.hasBoundedHeight) constraints.maxHeight else Constraints.Infinity,
                minHeight = constraints.minWidth,
                maxHeight = if (constraints.hasBoundedWidth) constraints.maxWidth else Constraints.Infinity
            )
            val placeable = measurable.measure(swappedConstraints)
            layout(placeable.height, placeable.width) {
                placeable.place(
                    x = (placeable.height - placeable.width) / 2,
                    y = (placeable.width - placeable.height) / 2
                )
            }
        } else {
            val placeable = measurable.measure(constraints)
            layout(placeable.width, placeable.height) {
                placeable.place(0, 0)
            }
        }
    }
}
