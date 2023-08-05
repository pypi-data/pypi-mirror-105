from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class Medication_IngredientSchema:
    """
    This resource is primarily used for the identification and definition of a
    medication. It covers the ingredients and the packaging for a medication.
    """
    # noinspection PyDefaultArgument
    @staticmethod
    def get_schema(
        max_nesting_depth: Optional[int] = 6,
        nesting_depth: int = 0,
        nesting_list: List[str] = [],
        max_recursion_limit: Optional[int] = 2,
        include_extension: Optional[bool] = False
    ) -> Union[StructType, DataType]:
        """
        This resource is primarily used for the identification and definition of a
        medication. It covers the ingredients and the packaging for a medication.


        itemCodeableConcept: The actual ingredient - either a substance (simple ingredient) or another
            medication.

        itemReference: The actual ingredient - either a substance (simple ingredient) or another
            medication.

        isActive: Indication of whether this ingredient affects the therapeutic action of the
            drug.

        amount: Specifies how many (or how much) of the items there are in this Medication.
            For example, 250 mg per tablet.  This is expressed as a ratio where the
            numerator is 250mg and the denominator is 1 tablet.

        """
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.ratio import RatioSchema
        if (
            max_recursion_limit and
            nesting_list.count("Medication_Ingredient") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Medication_Ingredient"]
        schema = StructType(
            [
                # The actual ingredient - either a substance (simple ingredient) or another
                # medication.
                StructField(
                    "itemCodeableConcept",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The actual ingredient - either a substance (simple ingredient) or another
                # medication.
                StructField(
                    "itemReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Indication of whether this ingredient affects the therapeutic action of the
                # drug.
                StructField("isActive", BooleanType(), True),
                # Specifies how many (or how much) of the items there are in this Medication.
                # For example, 250 mg per tablet.  This is expressed as a ratio where the
                # numerator is 250mg and the denominator is 1 tablet.
                StructField(
                    "amount",
                    RatioSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
