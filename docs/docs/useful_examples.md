# Useful Examples

The use of jinja in tweaks files adds a lot of flexibility. Here are some advanced examples of common tasks being automated with jinja.

## Generating an XY Matrix
```yaml
{#
Basic XY matrix example.
Min is lowest strength, max is highest strength.
Step is the step size between each strength value.
#}

{% set min = 0 %}
{% set max = 1 %}
{% set step = 0.1 %}

{% macro lora1_strength(iteration) -%}
    {{- min + (iteration // ((max - min) / step)) * step -}}
{%- endmacro %}

{% macro lora2_strength(iteration) -%}
    {{- min + (iteration % ((max - min) / step)) * step -}}
{%- endmacro %}
tweaks:
    - selector:
        name: "Lora Loader 1"
      changes:
        model_strength: {{ lora1_strength(iteration) }}
    - selector:
        name: "Lora Loader 2"
      changes:
        model_strength: {{ lora2_strength(iteration) }}
    - selector:
        name: "KSampler"
      changes:
        seed: {{random_seed()}}
    - selector:
        name: "Save Image"
      changes:
        prefix : "lora1_{{ lora1_strength(iteration) }}_lora2_{{ lora2_strength(iteration) }}_image"
```