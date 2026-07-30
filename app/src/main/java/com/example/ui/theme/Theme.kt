package com.example.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightBlueColorScheme = lightColorScheme(
    primary = LightBluePrimary,
    onPrimary = LightBlueOnPrimary,
    background = LightBlueBackground,
    onBackground = LightBlueOnBackground,
    surface = LightBlueSurface,
    onSurface = LightBlueOnSurface,
    surfaceVariant = LightBlueSurfaceVariant,
    onSurfaceVariant = LightBlueOnSurfaceVariant,
    primaryContainer = LightBluePrimaryContainer,
    onPrimaryContainer = LightBlueOnPrimaryContainer,
    surfaceTint = LightBlueSurface,
    surfaceContainer = LightBlueSurface,
    surfaceContainerHigh = LightBlueSurface,
    surfaceContainerHighest = LightBlueSurface,
    surfaceContainerLow = LightBlueSurface,
    surfaceContainerLowest = LightBlueSurface
)

@Composable
fun MyApplicationTheme(
    content: @Composable () -> Unit
) {
    MaterialTheme(
        colorScheme = LightBlueColorScheme,
        typography = Typography,
        content = content
    )
}
