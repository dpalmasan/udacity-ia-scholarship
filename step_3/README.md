# Step 2

In this step do the following tasks:

* Upload a vídeo to Vídeo Indexer using the API
* Extract face thumbnails from the vídeo and saving into disk
* Get sentiments and emotions from the person in the video
* Get faces from fake CA driver's license
* Check if the face in the CA driver's license matches the person in the video

## Experiments

I firstly tried a video using glasses, I got these results (video person is `ca-dl-diogo`). It seems it has more confidence relative to the other persons, but still not sufficient to assert that the person in the id is the same that the one on the video.

```
2022-05-05 06:12:47,391 video  INFO Comparing human-face4 to ca-dl-clynton
2022-05-05 06:12:47,391 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.18596.
2022-05-05 06:12:47,519 video  INFO Comparing human-face4 to ca-dl-diogo
2022-05-05 06:12:47,519 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.41758.
2022-05-05 06:12:47,626 video  INFO Comparing human-face4 to ca-dl-javiera
2022-05-05 06:12:47,626 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.09481.
2022-05-05 06:12:47,733 video  INFO Comparing human-face4 to ca-dl-manuel
2022-05-05 06:12:47,733 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.10889.
2022-05-05 06:12:47,841 video  INFO Comparing human-face4 to ca-dl-norma
2022-05-05 06:12:47,842 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.08895.
```

After I took off the glasses, I get the expected result, that the person in the vídeo matches with `ca-dl-diogo`:

```
2022-05-05 06:25:55,242 video  INFO Comparing human-face4 to ca-dl-clynton
2022-05-05 06:25:55,242 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.09248.
2022-05-05 06:25:55,347 video  INFO Comparing human-face4 to ca-dl-diogo
2022-05-05 06:25:55,347 video  INFO Faces are of the same (Positive) person, similarity confidence: 0.67677.
2022-05-05 06:25:55,453 video  INFO Comparing human-face4 to ca-dl-javiera
2022-05-05 06:25:55,453 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.10802.
2022-05-05 06:25:55,555 video  INFO Comparing human-face4 to ca-dl-manuel
2022-05-05 06:25:55,555 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.20308.
2022-05-05 06:25:55,662 video  INFO Comparing human-face4 to ca-dl-norma
2022-05-05 06:25:55,663 video  INFO Faces are of different (Negative) persons, similarity confidence: 0.09895.
```