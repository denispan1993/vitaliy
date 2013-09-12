Options

There are several options you can modify. First and most important is the step parameter. Step parameter defines how many child items will be visible at a time. It is also used in calculating of number of pages. By default this parameter is set to 4. To use your own step value, change the step parameter:

jQuery(function($){
  
  $('ul#items').easyPaginate({
  step:3
  });
  
}); 

Here’s the full list of available options:
step

Default value: 4
Defines a number of items visible on each "page".
delay

Default value: 100
Items on each "page" fade in one by one. This parameter controls the pause between each item’s appearance so we can create "wave" effect. It is defined in milliseconds.
numeric

Default value: true
Boolean. If set to true then the numeric pagination buttons will show.
nextprev

Default value: true
Boolean. If set to true then the next and previous pagination buttons will show.
auto

Default value: false
Boolean. If set to true then the plugin will automatically rotate the "pages"
pause

Default value: 4000
If set to auto pagination, this parameter controls the length of the pause in milliseconds between each "page turn".
clickstop

Default value: true
If set to auto pagination, this parameter controls whether the pages will continue to automatically rotate. If you want to continue the rotation set this parameter to false.
controls

Default value: ‘pagination’
As mentioned, the plugin generates an ordered list for the purpose of navigating through "pages". This parameter defines the list’s ID.
current

Default value: ‘current’
This parameter defines a class name of a current "page" in the numeric navigation. It is used for styling purposes.

If you want to create multiple paginations on the same page, have in mind that this plugin uses IDs to target control buttons so you need to define control id parameter for each pagination.