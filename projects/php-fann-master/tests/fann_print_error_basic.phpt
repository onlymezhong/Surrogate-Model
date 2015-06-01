--TEST--
Test function fann_reset_errno() by calling it with its expected arguments
--FILE--
<?php

$ann = fann_create_standard( 3, 2, 2, 1 );
fann_print_error( $ann );
echo "\n";
@fann_set_activation_function_layer( $ann, FANN_ELLIOT, 3 );
fann_print_error( $ann );

?>
--EXPECTF--
No error
%A