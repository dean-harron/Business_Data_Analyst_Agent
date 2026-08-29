# YouTube Analytics Guidance

For public YouTube Data API analysis, channel resources can provide metadata, statistics, and the uploads playlist. The uploads playlist can then be traversed to obtain video IDs, after which video statistics can be retrieved. Public data should not be treated as a substitute for private YouTube Analytics data.

Recommended analyses:
- views by publication month
- views per day since publication where timestamps permit
- like rate = likes / views
- comment rate = comments / views
- upload cadence
- performance distribution and outliers
- title/topic clusters when text data is available
- relationship between upload frequency and output

Avoid causal claims unless the design supports them.
