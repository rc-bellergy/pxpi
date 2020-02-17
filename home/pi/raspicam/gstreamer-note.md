# gstreamer notes:

## The raspivid to gstreamer

From: raspivid source
---
`fdsrc`
> src: ANY
---
`h264parse`
> sink: video/x-h264:
> src:  video/x-h264:
        parsed: true
        stream-format: avc
        alignment: au
---
`rtph264pay`
> sink: video/x-h264:
        stream-format: avc
        alignment: au
> src:  application/x-rtp:
        media: video
        payload: [ 96, 127 ]
        clock-rate: 90000
        encoding-name: H264
---
`udpsink`
> sink: ANY
---
To: video player


## The direct camera to gstreamer

From: camera source
---
`v4l2src`
> src:  video/x-h264:
        stream-format: avc
        alignment: au
---
`rtph264pay`
> sink: video/x-h264:
        stream-format: avc
        alignment: au
> src:  application/x-rtp:
        media: video
        payload: [ 96, 127 ]
        clock-rate: 90000
        encoding-name: H264
---
`udpsink`
> sink: ANY
---
To: video player
