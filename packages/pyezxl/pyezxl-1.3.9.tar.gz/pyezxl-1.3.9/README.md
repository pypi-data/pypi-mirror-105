This module is for easily read/write with EXCEL using Python.

The target is for easily control for EXCEL.

Therefore pyezxl is focused to control easily as follows.

1) the function name is consist of 3 parts (action_target_role)
   
   read_range_value
   
   write_cell_value
   
   delete_cell_value

2) function name is linked with underbar(_) and text is all lowcase
   
   action words : read, write, Insert, delete, change, set, copy, move
   
   target words : range, sheet, x, y, line
   
   role words : name, color, value, end

3) word definition
   
  * read: when you want to read cell value

     check : read some data except cell value as like color, font etc

  * write : when you want to write cell value

    set : write some data except cell value as like color, line etc

  * cell : 1 cell

    range : minimum 2 cells and over