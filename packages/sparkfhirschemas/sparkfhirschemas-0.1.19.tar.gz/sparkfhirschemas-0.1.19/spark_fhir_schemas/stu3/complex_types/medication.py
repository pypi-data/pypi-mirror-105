from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import BooleanType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class MedicationSchema:
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


        resourceType: This is a Medication resource

        code: A code (or set of codes) that specify this medication, or a textual
            description if no code is available. Usage note: This could be a standard
            medication code such as a code from RxNorm, SNOMED CT, IDMP etc. It could also
            be a national or local formulary code, optionally with translations to other
            code systems.

        status: A code to indicate if the medication is in active use.

        isBrand: Set to true if the item is attributable to a specific manufacturer.

        isOverTheCounter: Set to true if the medication can be obtained without an order from a
            prescriber.

        manufacturer: Describes the details of the manufacturer of the medication product.  This is
            not intended to represent the distributor of a medication product.

        form: Describes the form of the item.  Powder; tablets; capsule.

        ingredient: Identifies a particular constituent of interest in the product.

        package: Information that only applies to packages (not products).

        image: Photo(s) or graphic representation(s) of the medication.

        """
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.medication_ingredient import Medication_IngredientSchema
        from spark_fhir_schemas.stu3.complex_types.medication_package import Medication_PackageSchema
        from spark_fhir_schemas.stu3.complex_types.attachment import AttachmentSchema
        if (
            max_recursion_limit
            and nesting_list.count("Medication") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Medication"]
        schema = StructType(
            [
                # This is a Medication resource
                StructField("resourceType", StringType(), True),
                # A code (or set of codes) that specify this medication, or a textual
                # description if no code is available. Usage note: This could be a standard
                # medication code such as a code from RxNorm, SNOMED CT, IDMP etc. It could also
                # be a national or local formulary code, optionally with translations to other
                # code systems.
                StructField(
                    "code",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A code to indicate if the medication is in active use.
                StructField("status", StringType(), True),
                # Set to true if the item is attributable to a specific manufacturer.
                StructField("isBrand", BooleanType(), True),
                # Set to true if the medication can be obtained without an order from a
                # prescriber.
                StructField("isOverTheCounter", BooleanType(), True),
                # Describes the details of the manufacturer of the medication product.  This is
                # not intended to represent the distributor of a medication product.
                StructField(
                    "manufacturer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Describes the form of the item.  Powder; tablets; capsule.
                StructField(
                    "form",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Identifies a particular constituent of interest in the product.
                StructField(
                    "ingredient",
                    ArrayType(
                        Medication_IngredientSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Information that only applies to packages (not products).
                StructField(
                    "package",
                    Medication_PackageSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Photo(s) or graphic representation(s) of the medication.
                StructField(
                    "image",
                    ArrayType(
                        AttachmentSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
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
