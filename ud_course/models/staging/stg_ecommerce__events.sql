WITH source AS (
	SELECT *

	FROM {{ source('thelook_ecommerce', 'events') }}
)

SELECT
	id AS event_id,
	user_id,
	sequence_number,
	session_id,
	created_at,
	ip_address,
	city,
	state,
	postal_code,
	browser,
	traffic_source,
	uri AS web_link,
	event_type,

	{{ get_brand_name('uri') }} AS brand_name


FROM source

{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
  -- (uses >= to allow for multiple runs on the same day)
  WHERE created_at >= (SELECT MAX(created_at) FROM {{ this }})

{% endif %}
