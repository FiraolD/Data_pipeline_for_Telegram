{{ config(materialized='table') }}

SELECT
    detection ->> 'label' AS object_class,
    ROUND((detection ->> 'confidence')::NUMERIC, 2) AS confidence_score,
    detection -> 'bbox' AS bounding_box,
    fid.image_path,
    fid.channel,
    fid.created_at
FROM public.fct_image_detections fid
CROSS JOIN JSONB_ARRAY_ELEMENTS(fid.detections) AS j(detection)
WHERE detection ->> 'label' IS NOT NULL