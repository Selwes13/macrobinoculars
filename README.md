# macrobinoculars
A raspberry pi project to feed the PiCamera input through image processing and out onto a screen for a Star Wars prop

## Process
- Read frame from Raspberry Pi camera
- Tranform frame to correct size and perform colour adjustments
- Push frame to built-in screen

## Speed testing
| Method | Frame Rate |
| --- | --- |
| All Python | 14fps |
| Write frame to file | 8fps |
| C Write to screen only | -fps |
