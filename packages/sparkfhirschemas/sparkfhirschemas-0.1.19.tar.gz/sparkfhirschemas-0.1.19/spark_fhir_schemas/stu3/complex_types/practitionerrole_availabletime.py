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
class PractitionerRole_AvailableTimeSchema:
    """
    A specific set of Roles/Locations/specialties/services that a practitioner may
    perform at an organization for a period of time.
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
        A specific set of Roles/Locations/specialties/services that a practitioner may
        perform at an organization for a period of time.


        daysOfWeek: Indicates which days of the week are available between the start and end
            Times.

        allDay: Is this always available? (hence times are irrelevant) e.g. 24 hour service.

        availableStartTime: The opening time of day. Note: If the AllDay flag is set, then this time is
            ignored.

        availableEndTime: The closing time of day. Note: If the AllDay flag is set, then this time is
            ignored.

        """
        if (
            max_recursion_limit
            and nesting_list.count("PractitionerRole_AvailableTime") >=
            max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + [
            "PractitionerRole_AvailableTime"
        ]
        schema = StructType(
            [
                # Indicates which days of the week are available between the start and end
                # Times.
                # Is this always available? (hence times are irrelevant) e.g. 24 hour service.
                StructField("allDay", BooleanType(), True),
                # The opening time of day. Note: If the AllDay flag is set, then this time is
                # ignored.
                StructField("availableStartTime", StringType(), True),
                # The closing time of day. Note: If the AllDay flag is set, then this time is
                # ignored.
                StructField("availableEndTime", StringType(), True),
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
