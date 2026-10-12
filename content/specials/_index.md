+++
title = "Specials"
kicker = "Limited Time"
description = "Rotating offers that sit outside the regular menu — night deals and one-offs, while they last."
weight = 90

# A special's photo is a page-bundle resource, so Hugo would publish the
# original into public/ verbatim even though nothing references it any more —
# monday-night-wings' 4000×3000 PNG alone was 13 MB, most of the deployed
# weight of this section. Each special's images go through dish-image.html,
# which publishes fingerprinted derivatives; the unprocessed original is dead
# weight. This stops only the originals from being copied out and leaves the
# derivatives (and the page itself) publishing normally. Done here rather than
# per page so a new special inherits it without remembering to.
[cascade.build]
  publishResources = false
+++