! Test Fortran COMPLEX wrapping and usage from Python with fmodpy.

SUBROUTINE TEST_STANDARD ( SING_IN , SING_OUT , ARRAY_IN , ARRAY_OUT , KNOWN_ARRAY_OUT , KNOWN_MATRIX_OUT , OPT_SING_IN , OPT_SING_OUT )
! Test the basic functionaly of the 'COMPLEX' type and its
! interoperability with Python. This includes, inputs, outputs,
! array inputs with known and unknown size, optional inputs, and
! optional outputs.
USE ISO_FORTRAN_ENV , ONLY : REAL128
USE ISO_FORTRAN_ENV , ONLY : REAL128
IMPLICIT NONE
! Argument definitions.
COMPLEX ( KIND = REAL128 ) , INTENT ( IN ) : : SING_IN
COMPLEX ( KIND = REAL128 ) , INTENT ( OUT ) : : SING_OUT
COMPLEX ( KIND = REAL128 ) , DIMENSION ( : ) , INTENT ( IN ) : : ARRAY_IN
COMPLEX ( KIND = REAL128 ) , DIMENSION ( : ) , INTENT ( OUT ) : : ARRAY_OUT
COMPLEX ( KIND = REAL128 ) , DIMENSION ( SIZE ( ARRAY_OUT ) ) , INTENT ( OUT ) : : KNOWN_ARRAY_OUT
COMPLEX ( KIND = REAL128 ) , DIMENSION ( 3 , SIZE ( ARRAY_OUT ) ) , INTENT ( OUT ) : : KNOWN_MATRIX_OUT
COMPLEX ( KIND = REAL128 ) , INTENT ( IN ) , OPTIONAL : : OPT_SING_IN
COMPLEX ( KIND = REAL128 ) , INTENT ( OUT ) , OPTIONAL : : OPT_SING_OUT
! Local variable.
INTEGER : : I
! Copy the single input value to the single output value.
! Copy as much of the input array as possible to the output array.
! Set the KNOWN_ARRAY and the KNOWN_MATRIX values to be identifiabl.
! Do some operations on the optional inputs / outputs.
! End of this subroutine.
END SUBROUTINE TEST_STANDARD


FUNCTION TEST_EXTENDED ( OPT_ARRAY_IN , KNOWN_OPT_ARRAY_OUT , OPT_ALLOC_ARRAY_OUT , N ) RESULT ( ALLOC_ARRAY_OUT )
! Test the extended functionaly of the 'COMPLEX' type and its
! interoperability with Python. This includes, optional array
! inputs, optional array outputs, and allocatable array outputs.
USE ISO_FORTRAN_ENV , ONLY : REAL128
IMPLICIT NONE
COMPLEX ( KIND = REAL128 ) , INTENT ( IN ) , OPTIONAL , DIMENSION ( : ) : : OPT_ARRAY_IN
COMPLEX ( KIND = REAL128 ) , INTENT ( OUT ) , OPTIONAL : : KNOWN_OPT_ARRAY_OUT ( 3 )
COMPLEX ( KIND = REAL128 ) , INTENT ( OUT ) , OPTIONAL , ALLOCATABLE : : OPT_ALLOC_ARRAY_OUT ( : )
COMPLEX ( KIND = REAL128 ) , DIMENSION ( : ) , ALLOCATABLE : : ALLOC_ARRAY_OUT
INTEGER , INTENT ( IN ) : : N
! Local variable.
INTEGER : : I

! Assign the optional array output values.

! Allocate the optional array output and assign its values.

! Allocate the required array output to the specified size.

! End of function.
END FUNCTION TEST_EXTENDED