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
class EligibilityRequestSchema:
    """
    The EligibilityRequest provides patient and insurance coverage information to
    an insurer for them to respond, in the form of an EligibilityResponse, with
    information regarding whether the stated coverage is valid and in-force and
    optionally to provide the insurance details of the policy.
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
        The EligibilityRequest provides patient and insurance coverage information to
        an insurer for them to respond, in the form of an EligibilityResponse, with
        information regarding whether the stated coverage is valid and in-force and
        optionally to provide the insurance details of the policy.


        resourceType: This is a EligibilityRequest resource

        identifier: The Response business identifier.

        status: The status of the resource instance.

        priority: Immediate (STAT), best effort (NORMAL), deferred (DEFER).

        patient: Patient Resource.

        servicedDate: The date or dates when the enclosed suite of services were performed or
            completed.

        servicedPeriod: The date or dates when the enclosed suite of services were performed or
            completed.

        created: The date when this resource was created.

        enterer: Person who created the invoice/claim/pre-determination or pre-authorization.

        provider: The practitioner who is responsible for the services rendered to the patient.

        organization: The organization which is responsible for the services rendered to the
            patient.

        insurer: The Insurer who is target  of the request.

        facility: Facility where the services were provided.

        coverage: Financial instrument by which payment information for health care.

        businessArrangement: The contract number of a business agreement which describes the terms and
            conditions.

        benefitCategory: Dental, Vision, Medical, Pharmacy, Rehab etc.

        benefitSubCategory: Dental: basic, major, ortho; Vision exam, glasses, contacts; etc.

        """
        from spark_fhir_schemas.stu3.complex_types.identifier import IdentifierSchema
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        if (
            max_recursion_limit
            and nesting_list.count("EligibilityRequest") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["EligibilityRequest"]
        schema = StructType(
            [
                # This is a EligibilityRequest resource
                StructField("resourceType", StringType(), True),
                # The Response business identifier.
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
                # The status of the resource instance.
                StructField("status", StringType(), True),
                # Immediate (STAT), best effort (NORMAL), deferred (DEFER).
                StructField(
                    "priority",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Patient Resource.
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
                # The date or dates when the enclosed suite of services were performed or
                # completed.
                StructField("servicedDate", StringType(), True),
                # The date or dates when the enclosed suite of services were performed or
                # completed.
                StructField(
                    "servicedPeriod",
                    PeriodSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The date when this resource was created.
                StructField("created", StringType(), True),
                # Person who created the invoice/claim/pre-determination or pre-authorization.
                StructField(
                    "enterer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The practitioner who is responsible for the services rendered to the patient.
                StructField(
                    "provider",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The organization which is responsible for the services rendered to the
                # patient.
                StructField(
                    "organization",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The Insurer who is target  of the request.
                StructField(
                    "insurer",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Facility where the services were provided.
                StructField(
                    "facility",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Financial instrument by which payment information for health care.
                StructField(
                    "coverage",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The contract number of a business agreement which describes the terms and
                # conditions.
                StructField("businessArrangement", StringType(), True),
                # Dental, Vision, Medical, Pharmacy, Rehab etc.
                StructField(
                    "benefitCategory",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Dental: basic, major, ortho; Vision exam, glasses, contacts; etc.
                StructField(
                    "benefitSubCategory",
                    CodeableConceptSchema.get_schema(
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
