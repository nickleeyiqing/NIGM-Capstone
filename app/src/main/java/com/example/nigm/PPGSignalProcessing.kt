package com.example.nigm

object PPGSignalProcessor {
    // Define an array or list to store red channel values from PPG
    var redChannelValues: MutableList<Float> = mutableListOf()

    // Add a function to process the PPG signal and populate the redChannelValues
    fun processPPGSignal(data: ByteArray) {
        // Process the data and extract red channel values
        // This is just a placeholder, your actual signal processing will depend on how you're capturing the data
        for (i in data.indices) {
            val redValue = data[i].toFloat()  // Example of extracting red channel values
            redChannelValues.add(redValue)
        }
    }

    // Function to clear previous values (if needed)
    fun reset() {
        redChannelValues.clear()
    }
}
