/* 
This javascript is for shading cells on leader lists. 
This will adjust cell colors after the page loads based on class names.
It is case sensitive.
*/
 
$(document).ready(function() {
	$( "span:contains('Rogue')" ).parent().css("background-color", "#c09a27");
	$( "span:contains('Primalist')" ).parent().css("background-color", "#0b5394");
	$( "span:contains('Warrior')" ).parent().css("background-color", "#CC0000");
	$( "span:contains('Mage')" ).parent().css("background-color", "purple");
	$( "span:contains('Cleric')" ).parent().css("background-color", "green");

	$( "tr:contains('Azranel')" ).css("background-color", "#031729");
	$( "tr:contains('Vindicator MK1')" ).css("background-color", "#04223d");
	$( "tr:contains('Commander Isiel')" ).css("background-color", "#073966");
	$( "tr:contains('Titan X')" ).css("background-color", "#114652");
	
});

