#include "FastLED.h"

#define NUM_LEDS 104
#define LED_PIN 6 // Any PWM pin
#define NUM_BYTES (NUM_LEDS*3) // 3 colors  

#define BRIGHTNESS 50

int led_counter = 0;
int byte_counter = 0;

CRGB leds[NUM_LEDS];
byte buffer[NUM_BYTES];
byte buffer2[NUM_BYTES];

void setup() {
  // Serial setup
  Serial.begin(115200); // Use the same baud-rate as the python side
  Serial.setTimeout(500); 

  // FastLED setup
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}

void loop() {
  getScreenData();  
}

void getScreenData() {
  // Communication with python script. Flag to request data.
  Serial.write(0); 

  //delay(10); // For debugging

  // Read in all RGB values of each LED
  Serial.readBytes(buffer, NUM_LEDS * 3); 

  // Set all LED colors
  while (byte_counter < NUM_LEDS * 3)
  {
    byte red = buffer[byte_counter++];
    byte green = buffer[byte_counter++];
    byte blue = buffer[byte_counter++];

    leds[led_counter++] = CRGB(red, green, blue);
  }

  // Display
  FastLED.show();

  // Reset for next frame
  byte_counter = 0;
  led_counter = 0;
}
