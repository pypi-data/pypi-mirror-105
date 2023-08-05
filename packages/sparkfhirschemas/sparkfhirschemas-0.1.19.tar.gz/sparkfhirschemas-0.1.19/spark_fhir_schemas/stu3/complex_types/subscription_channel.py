from typing import List
from typing import Optional
from typing import Union

from pyspark.sql.types import DataType
from pyspark.sql.types import StringType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType


# This file is auto-generated by generate_schema so do not edit manually
# noinspection PyPep8Naming
class Subscription_ChannelSchema:
    """
    The subscription resource is used to define a push based subscription from a
    server to another system. Once a subscription is registered with the server,
    the server checks every resource that is created or updated, and if the
    resource matches the given criteria, it sends a message on the defined
    "channel" so that another system is able to take an appropriate action.
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
        The subscription resource is used to define a push based subscription from a
        server to another system. Once a subscription is registered with the server,
        the server checks every resource that is created or updated, and if the
        resource matches the given criteria, it sends a message on the defined
        "channel" so that another system is able to take an appropriate action.


        type: The type of channel to send notifications on.

        endpoint: The uri that describes the actual end-point to send messages to.

        payload: The mime type to send the payload in - either application/fhir+xml, or
            application/fhir+json. If the payload is not present, then there is no payload
            in the notification, just a notification.

        header: Additional headers / information to send as part of the notification.

        """
        if (
            max_recursion_limit and
            nesting_list.count("Subscription_Channel") >= max_recursion_limit
        ) or (max_nesting_depth and nesting_depth >= max_nesting_depth):
            return StructType([StructField("id", StringType(), True)])
        # add my name to recursion list for later
        my_nesting_list: List[str] = nesting_list + ["Subscription_Channel"]
        schema = StructType(
            [
                # The type of channel to send notifications on.
                StructField("type", StringType(), True),
                # The uri that describes the actual end-point to send messages to.
                StructField("endpoint", StringType(), True),
                # The mime type to send the payload in - either application/fhir+xml, or
                # application/fhir+json. If the payload is not present, then there is no payload
                # in the notification, just a notification.
                StructField("payload", StringType(), True),
                # Additional headers / information to send as part of the notification.
            ]
        )
        if not include_extension:
            schema.fields = [
                c if c.name != "extension" else
                StructField("extension", StringType(), True)
                for c in schema.fields
            ]
        return schema
