Because the examples show that the output grid is largely a modified version of the input grid, it's best to initialize the output grid using `initialize_output_from_input`. This function will create a copy of the input grid, making it easier to modify individual pixels.  The modifications are focused additions around already existing pixels.  A fresh grid is not appropriate because it would require setting all pixels instead of just adding a few.


