package com.example.nigm

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView
import com.example.nigm.ui.theme.NIGMTheme
import com.github.mikephil.charting.charts.LineChart
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.github.mikephil.charting.components.Description

class GraphActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            NIGMTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    GraphScreen()
                }
            }
        }
    }

    @Composable
    fun GraphScreen() {
        // Create a LineChart object for visualizing PPG signal
        AndroidView(factory = { context ->
            val chart = LineChart(context)  // Create a LineChart instance

            // Create entries for the chart using redChannelValues from PPGSignalProcessor
            val entries = ArrayList<Entry>()
            for (i in 0 until PPGSignalProcessor.redChannelValues.size) {
                val value = PPGSignalProcessor.redChannelValues[i]
                entries.add(Entry(i.toFloat(), value))
            }

            // Create a dataset for the chart
            val lineDataSet = LineDataSet(entries, "PPG Signal")
            val lineData = LineData(lineDataSet)

            // Customize chart
            chart.data = lineData
            chart.description.text = "PPG Signal over Time"
            chart.invalidate() // Refresh the chart

            chart  // Return the chart
        })
    }
}
