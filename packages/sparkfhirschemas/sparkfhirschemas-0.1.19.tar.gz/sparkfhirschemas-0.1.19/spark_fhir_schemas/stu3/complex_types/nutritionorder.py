from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class NutritionOrderSchema:
    """
    A request to supply a diet, formula feeding (enteral) or oral nutritional
    supplement to a patient/resident.
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
        A request to supply a diet, formula feeding (enteral) or oral nutritional
        supplement to a patient/resident.


        resourceType: This is a NutritionOrder resource

        identifier: Identifiers assigned to this order by the order sender or by the order
            receiver.

        status: The workflow status of the nutrition order/request.

        patient: The person (patient) who needs the nutrition order for an oral diet,
            nutritional supplement and/or enteral or formula feeding.

        encounter: An encounter that provides additional information about the healthcare context
            in which this request is made.

        dateTime: The date and time that this nutrition order was requested.

        orderer: The practitioner that holds legal responsibility for ordering the diet,
            nutritional supplement, or formula feedings.

        allergyIntolerance: A link to a record of allergies or intolerances  which should be included in
            the nutrition order.

        foodPreferenceModifier: This modifier is used to convey order-specific modifiers about the type of
            food that should be given. These can be derived from patient allergies,
            intolerances, or preferences such as Halal, Vegan or Kosher. This modifier
            applies to the entire nutrition order inclusive of the oral diet, nutritional
            supplements and enteral formula feedings.

        excludeFoodModifier: This modifier is used to convey order-specific modifiers about the type of
            food that should NOT be given. These can be derived from patient allergies,
            intolerances, or preferences such as No Red Meat, No Soy or No Wheat or
            Gluten-Free.  While it should not be necessary to repeat allergy or
            intolerance information captured in the referenced AllergyIntolerance resource
            in the excludeFoodModifier, this element may be used to convey additional
            specificity related to foods that should be eliminated from the patient’s diet
            for any reason.  This modifier applies to the entire nutrition order inclusive
            of the oral diet, nutritional supplements and enteral formula feedings.

        oralDiet: Diet given orally in contrast to enteral (tube) feeding.

        supplement: Oral nutritional products given in order to add further nutritional value to
            the patient's diet.

        enteralFormula: Feeding provided through the gastrointestinal tract via a tube, catheter, or
            stoma that delivers nutrition distal to the oral cavity.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.nutritionorder_oraldiet import NutritionOrder_OralDietSchema
        from spark_fhir_schemas.stu3.complex_types.nutritionorder_supplement import NutritionOrder_SupplementSchema
        from spark_fhir_schemas.stu3.complex_types.nutritionorder_enteralformula import NutritionOrder_EnteralFormulaSchema
        if (
            max_recursion_limit
            and nesting_list.count("NutritionOrder") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["NutritionOrder"]
        schema = StructType(
            [
                # This is a NutritionOrder resource
                StructField("resourceType", StringType(), True),
                # Identifiers assigned to this order by the order sender or by the order
                # receiver.
                StructField(
                    "identifier",
                    ArrayType(
                        IdentifierSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # The workflow status of the nutrition order/request.
                StructField("status", StringType(), True),
                # The person (patient) who needs the nutrition order for an oral diet,
                # nutritional supplement and/or enteral or formula feeding.
                StructField(
                    "patient",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # An encounter that provides additional information about the healthcare context
                # in which this request is made.
                StructField(
                    "encounter",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The date and time that this nutrition order was requested.
                StructField("dateTime", StringType(), True),
                # The practitioner that holds legal responsibility for ordering the diet,
                # nutritional supplement, or formula feedings.
                StructField(
                    "orderer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A link to a record of allergies or intolerances  which should be included in
                # the nutrition order.
                StructField(
                    "allergyIntolerance",
                    ArrayType(
                        ReferenceSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # This modifier is used to convey order-specific modifiers about the type of
                # food that should be given. These can be derived from patient allergies,
                # intolerances, or preferences such as Halal, Vegan or Kosher. This modifier
                # applies to the entire nutrition order inclusive of the oral diet, nutritional
                # supplements and enteral formula feedings.
                StructField(
                    "foodPreferenceModifier",
                    ArrayType(
                        CodeableConceptSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # This modifier is used to convey order-specific modifiers about the type of
                # food that should NOT be given. These can be derived from patient allergies,
                # intolerances, or preferences such as No Red Meat, No Soy or No Wheat or
                # Gluten-Free.  While it should not be necessary to repeat allergy or
                # intolerance information captured in the referenced AllergyIntolerance resource
                # in the excludeFoodModifier, this element may be used to convey additional
                # specificity related to foods that should be eliminated from the patient’s diet
                # for any reason.  This modifier applies to the entire nutrition order inclusive
                # of the oral diet, nutritional supplements and enteral formula feedings.
                StructField(
                    "excludeFoodModifier",
                    ArrayType(
                        CodeableConceptSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Diet given orally in contrast to enteral (tube) feeding.
                StructField(
                    "oralDiet",
                    NutritionOrder_OralDietSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Oral nutritional products given in order to add further nutritional value to
                # the patient's diet.
                StructField(
                    "supplement",
                    ArrayType(
                        NutritionOrder_SupplementSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Feeding provided through the gastrointestinal tract via a tube, catheter, or
                # stoma that delivers nutrition distal to the oral cavity.
                StructField(
                    "enteralFormula",
                    NutritionOrder_EnteralFormulaSchema.get_schema(
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
