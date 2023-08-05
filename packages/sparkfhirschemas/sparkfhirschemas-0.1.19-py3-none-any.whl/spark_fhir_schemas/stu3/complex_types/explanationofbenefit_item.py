from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import ArrayType
from pyspark.sql.types import DataType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class ExplanationOfBenefit_ItemSchema:
    """
    This resource provides: the claim details; adjudication details from the
    processing of a Claim; and optionally account balance information, for
    informing the subscriber of the benefits provided.
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
        This resource provides: the claim details; adjudication details from the
        processing of a Claim; and optionally account balance information, for
        informing the subscriber of the benefits provided.


        sequence: A service line number.

        careTeamLinkId: Careteam applicable for this service or product line.

        diagnosisLinkId: Diagnosis applicable for this service or product line.

        procedureLinkId: Procedures applicable for this service or product line.

        informationLinkId: Exceptions, special conditions and supporting information pplicable for this
            service or product line.

        revenue: The type of reveneu or cost center providing the product and/or service.

        category: Health Care Service Type Codes  to identify the classification of service or
            benefits.

        service: If this is an actual service or product line, ie. not a Group, then use code
            to indicate the Professional Service or Product supplied (eg. CTP,
            HCPCS,USCLS,ICD10, NCPDP,DIN,ACHI,CCI). If a grouping item then use a group
            code to indicate the type of thing being grouped eg. 'glasses' or 'compound'.

        modifier: Item typification or modifiers codes, eg for Oral whether the treatment is
            cosmetic or associated with TMJ, or for medical whether the treatment was
            outside the clinic or out of office hours.

        programCode: For programs which require reson codes for the inclusion, covering, of this
            billed item under the program or sub-program.

        servicedDate: The date or dates when the enclosed suite of services were performed or
            completed.

        servicedPeriod: The date or dates when the enclosed suite of services were performed or
            completed.

        locationCodeableConcept: Where the service was provided.

        locationAddress: Where the service was provided.

        locationReference: Where the service was provided.

        quantity: The number of repetitions of a service or product.

        unitPrice: If the item is a node then this is the fee for the product or service,
            otherwise this is the total of the fees for the children of the group.

        factor: A real number that represents a multiplier used in determining the overall
            value of services delivered and/or goods received. The concept of a Factor
            allows for a discount or surcharge multiplier to be applied to a monetary
            amount.

        net: The quantity times the unit price for an addittional service or product or
            charge. For example, the formula: unit Quantity * unit Price (Cost per Point)
            * factor Number  * points = net Amount. Quantity, factor and points are
            assumed to be 1 if not supplied.

        udi: List of Unique Device Identifiers associated with this line item.

        bodySite: Physical service site on the patient (limb, tooth, etc).

        subSite: A region or surface of the site, eg. limb region or tooth surface(s).

        encounter: A billed item may include goods or services provided in multiple encounters.

        noteNumber: A list of note references to the notes provided below.

        adjudication: The adjudications results.

        detail: Second tier of goods and services.

        """
        from spark_fhir_schemas.stu3.complex_types.codeableconcept import CodeableConceptSchema
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        from spark_fhir_schemas.stu3.complex_types.address import AddressSchema
        from spark_fhir_schemas.stu3.complex_types.reference import ReferenceSchema
        from spark_fhir_schemas.stu3.complex_types.quantity import QuantitySchema
        from spark_fhir_schemas.stu3.complex_types.money import MoneySchema
        from spark_fhir_schemas.stu3.complex_types.explanationofbenefit_adjudication import ExplanationOfBenefit_AdjudicationSchema
        from spark_fhir_schemas.stu3.complex_types.explanationofbenefit_detail import ExplanationOfBenefit_DetailSchema
        if (
            max_recursion_limit
            and nesting_list.count("ExplanationOfBenefit_Item") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + [
            "ExplanationOfBenefit_Item"
        ]
        schema = StructType(
            [
                # A service line number.
                StructField("sequence", IntegerType(), True),
                # Careteam applicable for this service or product line.
                # Diagnosis applicable for this service or product line.
                # Procedures applicable for this service or product line.
                # Exceptions, special conditions and supporting information pplicable for this
                # service or product line.
                # The type of reveneu or cost center providing the product and/or service.
                StructField(
                    "revenue",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Health Care Service Type Codes  to identify the classification of service or
                # benefits.
                StructField(
                    "category",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If this is an actual service or product line, ie. not a Group, then use code
                # to indicate the Professional Service or Product supplied (eg. CTP,
                # HCPCS,USCLS,ICD10, NCPDP,DIN,ACHI,CCI). If a grouping item then use a group
                # code to indicate the type of thing being grouped eg. 'glasses' or 'compound'.
                StructField(
                    "service",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Item typification or modifiers codes, eg for Oral whether the treatment is
                # cosmetic or associated with TMJ, or for medical whether the treatment was
                # outside the clinic or out of office hours.
                StructField(
                    "modifier",
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
                # For programs which require reson codes for the inclusion, covering, of this
                # billed item under the program or sub-program.
                StructField(
                    "programCode",
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
                # Where the service was provided.
                StructField(
                    "locationCodeableConcept",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Where the service was provided.
                StructField(
                    "locationAddress",
                    AddressSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # Where the service was provided.
                StructField(
                    "locationReference",
                    ReferenceSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # The number of repetitions of a service or product.
                StructField(
                    "quantity",
                    QuantitySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # If the item is a node then this is the fee for the product or service,
                # otherwise this is the total of the fees for the children of the group.
                StructField(
                    "unitPrice",
                    MoneySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A real number that represents a multiplier used in determining the overall
                # value of services delivered and/or goods received. The concept of a Factor
                # allows for a discount or surcharge multiplier to be applied to a monetary
                # amount.
                StructField("factor", IntegerType(), True),
                # The quantity times the unit price for an addittional service or product or
                # charge. For example, the formula: unit Quantity * unit Price (Cost per Point)
                # * factor Number  * points = net Amount. Quantity, factor and points are
                # assumed to be 1 if not supplied.
                StructField(
                    "net",
                    MoneySchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # List of Unique Device Identifiers associated with this line item.
                StructField(
                    "udi",
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
                # Physical service site on the patient (limb, tooth, etc).
                StructField(
                    "bodySite",
                    CodeableConceptSchema.get_schema(
                        max_nesting_depth=max_nesting_depth,
                        nesting_depth=nesting_depth + 1,
                        nesting_list=my_nesting_list,
                        max_recursion_limit=max_recursion_limit,
                        include_extension=include_extension
                    ), True
                ),
                # A region or surface of the site, eg. limb region or tooth surface(s).
                StructField(
                    "subSite",
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
                # A billed item may include goods or services provided in multiple encounters.
                StructField(
                    "encounter",
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
                # A list of note references to the notes provided below.
                # The adjudications results.
                StructField(
                    "adjudication",
                    ArrayType(
                        ExplanationOfBenefit_AdjudicationSchema.get_schema(
                            max_nesting_depth=max_nesting_depth,
                            nesting_depth=nesting_depth + 1,
                            nesting_list=my_nesting_list,
                            max_recursion_limit=max_recursion_limit,
                            include_extension=include_extension
                        )
                    ), True
                ),
                # Second tier of goods and services.
                StructField(
                    "detail",
                    ArrayType(
                        ExplanationOfBenefit_DetailSchema.get_schema(
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
