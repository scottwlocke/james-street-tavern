+++
title = "Salads"
weight = 80

# Dish photos live in the item bundles now, and a bundle resource is copied
# into public/ verbatim unless a template uses it. The photos are only ever
# used through dish-image.html, which publishes fingerprinted derivatives, so
# this keeps the untouched 1600px originals off the deployed site. Cascaded
# from the section so every item inherits it.
[cascade.build]
  publishResources = false
+++
