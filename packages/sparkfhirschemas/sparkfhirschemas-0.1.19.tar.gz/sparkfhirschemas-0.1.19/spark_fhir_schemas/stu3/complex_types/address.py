from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class AddressSchema:
    """
    An address expressed using postal conventions (as opposed to GPS or other
    location definition formats).  This data type may be used to convey addresses
    for use in delivering mail as well as for visiting locations which might not
    be valid for mail delivery.  There are a variety of postal address formats
    defined around the world.
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
        An address expressed using postal conventions (as opposed to GPS or other
        location definition formats).  This data type may be used to convey addresses
        for use in delivering mail as well as for visiting locations which might not
        be valid for mail delivery.  There are a variety of postal address formats
        defined around the world.


        use: The purpose of this address.

        type: Distinguishes between physical addresses (those you can visit) and mailing
            addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.

        text: A full text representation of the address.

        line: This component contains the house number, apartment number, street name,
            street direction,  P.O. Box number, delivery hints, and similar address
            information.

        city: The name of the city, town, village or other community or delivery center.

        district: The name of the administrative area (county).

        state: Sub-unit of a country with limited sovereignty in a federally organized
            country. A code may be used if codes are in common use (i.e. US 2 letter state
            codes).

        postalCode: A postal code designating a region defined by the postal service.

        country: Country - a nation as commonly understood or generally accepted.

        period: Time period when address was/is in use.

        """
        from spark_fhir_schemas.stu3.complex_types.period import PeriodSchema
        if (
            max_recursion_limit
            and nesting_list.count("Address") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Address"]
        schema = StructType(
            [
                # The purpose of this address.
                StructField("use", StringType(), True),
                # Distinguishes between physical addresses (those you can visit) and mailing
                # addresses (e.g. PO Boxes and care-of addresses). Most addresses are both.
                StructField("type", StringType(), True),
                # A full text representation of the address.
                StructField("text", StringType(), True),
                # This component contains the house number, apartment number, street name,
                # street direction,  P.O. Box number, delivery hints, and similar address
                # information.
                # The name of the city, town, village or other community or delivery center.
                StructField("city", StringType(), True),
                # The name of the administrative area (county).
                StructField("district", StringType(), True),
                # Sub-unit of a country with limited sovereignty in a federally organized
                # country. A code may be used if codes are in common use (i.e. US 2 letter state
                # codes).
                StructField("state", StringType(), True),
                # A postal code designating a region defined by the postal service.
                StructField("postalCode", StringType(), True),
                # Country - a nation as commonly understood or generally accepted.
                StructField("country", StringType(), True),
                # Time period when address was/is in use.
                StructField(
                    "period",
                    PeriodSchema.get_schema(
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
