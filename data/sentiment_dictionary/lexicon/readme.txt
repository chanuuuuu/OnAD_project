한국어 감정 어휘 목록

이 어휘 목록은 KOSAC 데이터를 한국어 감정 분석 연구에 폭넓게 활용할 수 있도록 형태소 단위의 감정 특성을 제공하는 것을 목적으로 한다. 여기서는 어휘의 감정 특성이 그 어휘를 포함하는 핵심 주관 표현(이하 Seed)의 감정 특성에서 도출될 수 있다고 가정하고, Seed에서 추출한 형태소 N-그램을 어휘 표제어로 삼았다. 단, 한 Seed가 다른 Seed를 포함하는 경우 상위 Seed가 하위 Seed를 인용하거나 부정하거나 강조하는 등의 방식으로 감정 특성값을 전환할 수 있으므로, 일관된 감정 특성값을 얻기 위해 다른 Seed와 중첩되지 않는 최하위 Seed에 포함된 형태소만을 사용하였다. 형태소 N-그램은 가능한 모든 것을 뽑되 한글 이외의 문자나 문장 부호가 포함된 것은 제외하였다. 여섯 가지 의미 특성의 종류 및 값의 설명은 KOSAC V 1.0 README 파일에서 볼 수 있다. 

lexicon.zip에 포함된 csv 파일 여섯 개는 각각 의미 특성 하나에 해당하며, 위에서 서술한 방식으로 얻은 형태소 N-그램 표제어 16,362개(유니그램 3,476개, 바이그램 6,579개, 트라이그램 6,307개)가 가지는 의미 특성값들의 분포로 구성되어 있다. 파일 내에서 각 행은 하나의 N-그램의 감정 특성을 가리킨다. 열에 해당하는 값의 의미는 순서대로 다음과 같다.

	- ngram: 표제어 N-그램을 이루는 형태소
	- freq: 해당 N-그램을 포함하는 Seed의 개수
	- (의미 특성값): 해당 N-그램을 포함하는 Seed 중 이 값을 가지는 것들의 비율
	- max.value: 가장 높은 비율을 차지하는 값의 이름
	- max.prop: 가장 높은 비율의 수치

The KOSAC data in the csv formatted file contains all annotated tags: subjective, objective, and seed tags.

This README is to provide a guide to understand the listed tags in csv format.
Each column is explained with number below.

***For detailed explanations of column values, see the guideline or Shin et al. (2012).

Shin, Hyopil, Munhyong Kim, Yu-Mi Jo, Hayeon Jang, and Andrew Cattle. 2012. 
Annotation Scheme for Constructing Sentiment Corpus in Korean In proceedings of 
the 26th Pacific Asia Conference on Language, Information and Compuation, pages 
181-190.

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

1. tag_id
This tag_id is unique ID for each tag in the whole KOSAC data.
The ID may not be continuous since some tags are deleted in annotation process.

2. sent_id
The sent_id refers to which sentence the tag belongs to.
Because the sentence ID is unique for each sentence, it helps to gather all 
tags that belong to it.

3. tag type
The tag type shows if the tag is a sentence level tag, subjective or objective, 
or an under-sentence level tag, seed tag.

4. morphemes
This column contains expressions on which tags are anchored. Only seed tags 
have anchored expressions on this column. Anchors of objective and subjective 
tags can be found on sentence-morph column. The format of each morpheme is 
expression/part_of_speech#id, as �쒖궗��/NNG#57926��. The id can be used to 
match the expression in the whole sentence.

5. expressive-type
The expressive-type column contains how the expression is delivered by a writer 
of the sentence. The values of the column are direct-explicit, direct-speech, 
direct-action, indirect, and writing-device.

6. subjectivity-type
The subjectivity-type attribute indicates what kind of sentiment the archored 
expression belongs to. The categories are Judgment, Argument, Intention, 
Agreement, Speculation, Emotion, Others.

7. subjectivity-polarity
The subjectivity-polarity has positive, negative, complex, and neutral. This 
value composes one united value with subjectivity-type value, for instance, 
judgment-pos, intention-pos. This value does not refer to the usual polarity 
sense of expressions. For more details, refer to the documents above.

8. polarity
The polarity attribute indicates the polarity sense of the anchored expression.

9. intensity
The intensity column shows the how strong the subjective expression is.

10. nested-source
This column shows the source of the expression and the path of the delivering 
subjectivity via sources. The left most source is always writer, though it is 
omitted. The format is source1-source2-source3. It is supposed that it is less 
likely to be the case that the sources of a subjective expression are more than 
four.

11. target
The target column contains the target expressions to which the direction of 
sentiment towards. The format is target1-target2-target3, indicating that 
multiple targets are possible for a sentiment expression.

12. comment
This column is for an annotator to leave a comment on a tag.

13. confident
This confident column is to leave a marker indicating how confident an 
annotator is about the tag.

14. raw-sentence
The raw-sentence column contains the original sentence that the tag belongs to.

15. sentence-morph
The raw-sentence column contains the original sentence with morphemes that the 
tag belongs to.