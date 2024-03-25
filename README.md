# autoUnderwaterOutfit
   
### Requirements:
  1. Python
    
    
#### Description:
  Python script for anime game to add auto outfit changing when under or in water. It will follow this logic. When entering water we store current outfit($swapvar value) and set the underwater outfit($UnderwaterOutfitSelect value). When leaving the water we set it back to the stored outfit($swapvar value). You can choose a toggle to enable/disable the functionality.
     

#### Update:
  1. Added a delay after leaving the water for when the outfit will switch back. Delay is counted by frames. The default is 480. At 30fps = 16 seconds and at 60fps = 8.
  2. You can customize the delay to your needs by running "autoUnderwaterOutfit.py --delay".
  3. Switching underwater outfits now uses the same key as switching main outfits.
  4. Adds support for global version of RemoveUnderwaterCensorship.


#### Update: 03/2024
  1. Added a delay when entering the water for when the outfit will switch. Delay is counted in seconds. The default is 0.00.
  2. If you want to set the delay you must use "autoUnderwaterOutfit.py --delay_start".
  3. For the delay when leaving the water use "autoUnderwaterOutfit.py --delay_end" (default is 9.75).
  5. Changed delay to count in seconds instead of frames. Should be more consistant no matter your fps.


     
##### How to Use:
  1. Place in the directory of the INI you want to adjust.
  2. Run the script(python autoUnderwaterOutfit.py) and you will be prompted to choose how many underwater outfits you have.
  3. Next you will have to choose what $swapvar values to use for the outfits.
  4. You will then be able to set a toggle key to enable/disable the functionality.
  5. Choose if you want the Underwater Outfits to only be available when you are underwater or if functionality is toggled off.
  6. Finaly the script will ask if you want to revert changes. So you can go in game and test it out.
      
      
##### Additional Usage:
  1. You can use commands to bypass inputs and set additional options. Run python "autoUnderwaterOutfit.py --help" to see available commands.
  2. If your ini file uses a different variable for "[KeyToggle]" or "$swapvar" you can open the script and change the values to work with your ini.

```
# Constants for section names
SWAPVAR_VARIABLE = $swapvar
KEYSWAP_SECTION = KeySwap.
```
