from pydantic import AliasGenerator
from pydantic.alias_generators import to_camel, to_snake


alias_generator_out = AliasGenerator(
  validation_alias=to_snake,
  serialization_alias=to_camel
)

alias_generator_in = AliasGenerator(
  validation_alias=to_camel,
  serialization_alias=to_camel,
)