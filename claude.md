# Game Boy Camera Processor

## Goal
A simple script to batch process all image files in a folder. BMP images, photos captured with a Game Boy DMG Camera. Photos should be upscaled and convert. Additionally I want to apply custom 4 color palletes.

## Pallets
Keep the definition of the color pallets simple so it's easy to add new palettes later.

## Flow
+ There is a "_inbox" where I will put the unprocessed BMP images
+ When processed move the original files to the "_original" folder

## Result
* Processed photos should be saved in a folder with a name by date
* different images saved in subfolders by pallete name

## Processing
* Applies differnt 4 color pallets
* Upscales without adding blurriness, keeping the scale factor clean to 400%
* Converts final image to png