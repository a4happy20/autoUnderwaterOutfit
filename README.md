# autoUnderwaterOutfit
   
### Requirements:
  1. Python
    
    
#### Description:
  Python script for anime game to add auto outfit changing when under or in water. It will follow this logic. When entering water we store current outfit($swapvar value) and set the underwater outfit($UnderwaterOutfitSelect value). When leaving the water we set it back to the stored outfit($swapvar value). You can choose a toggle to enable/disable the functionality. If you have more than one underwater outfit you can set a key to cycle through outfits.
     

#### Update:
  1. Added a delay after leaving the water for when the outfit will switch back. Delay is counted by frames. The default is 480. At 30fps = 16 seconds and at 60fps = 8.
  2. You can customize the delay to your needs by running "autoUnderwaterOutfit.py --delay".
  3. Switching underwater outfits now uses the same key as switching main outfits.
  4. Can choose to apply the shaderfix for characters from game version 3.0+.
       
     
##### How to Use:
  1. Place in the directory of the INI you want to adjust.
  2. Run the script(python autoUnderwaterOutfit.py) and you will be prompted to choose how many underwater outfits you have.
  3. Next you will have to choose what $swapvar values to use for the outfits.
  4. You will then be able to set a toggle key to enable/disable the functionality.
  5. Choose if you want the Underwater Outfits to only be available when you are underwater or if functionality is toggled off.
  6. Now you can apply the shader fix if your character is from game version 3.0 or above.
  6. Finaly the script will ask if you want to revert changes. So you can go in game and test it out.
      
      
##### Additional Usage:
  1. You can use commands to bypass inputs and set additional options. Run python "autoUnderwaterOutfit.py --help" to see available commands.
  2. If your ini file uses a different variable for "[KeyToggle]" or "$swapvar" you can open the script and change the values to work with your ini.

```
SWAPVAR_VARIABLE = $swapvar / KEYTOGGLE_SECTION = $keytoggle.
```
