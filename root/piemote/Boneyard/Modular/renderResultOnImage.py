def renderResultOnImage( result, img ):
        import operator
#Display the obtained results onto the input image

        for currFace in result:

                currEmotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]
                return currEmotion
