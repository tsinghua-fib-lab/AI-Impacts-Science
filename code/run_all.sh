python SelectWork_JournalConference.py
python SelectWork_Year_TitleAbstract_Language.py
# ~1 CPU days

python ClassifyWork_Title_Raw.py
python ClassifyWork_Abstract_Raw.py
python ClassifyWork_Title_Extend1.py
python ClassifyWork_Abstract_Extend1.py
python ClassifyWork_Union.py
python ClassifyWork_FilterNewData.py
# ~14 GPU days

python EmbedWork_AbstractTitle_Specter2.py
python EmbedWork_FilterNewData.py
# ~14 GPU days

python Get_Topic_Field_SubField.py
python Get_Institution_Info.py
python Get_Funder_Info.py
python Get_Source_Name.py
# ~2 CPU days

python Get_Work_Year.py
python Get_Work_Date.py
python Get_Work_Author.py
python Get_Work_Reference.py
python Get_Work_Topic.py
python Get_Work_Field.py
python Get_Work_SubField.py
python Get_Work_Grant.py
python Get_Work_IsReview.py
python Get_Work_IsData.py
python Get_Work_IsNanoSci.py
python Get_Work_PhraseLen2ByYear.py
python Get_Work_PhraseLen3ByYear.py
python Get_Work_PhraseLen2ByYear_AllFields.py
python Get_Work_PhraseLen3ByYear_AllFields.py
# ~7 CPU days

python Get_Author_Name.py
python Get_Author_Career.py
python Get_Author_Career_Date.py
python Get_Author_Field.py
python Get_Author_Institution.py
# ~3 CPU days

python Calculate_Work_TeamLast.py
python Calculate_Author_PaperByYear.py
python Calculate_Work_CoreReference.py
python Calculate_Work_Disruption.py
python Calculate_Work_CitationByYear.py
python Calculate_Work_CoreCitationByYear.py
python Calculate_Author_CitationByYear.py
# ~1 CPU days

python Calculate_Entropy_WorkField.py
python Calculate_Space_WorkField.py
python Calculate_Space_WorkSubField.py
python Calculate_Space_WorkTopic.py
python Calculate_Space_SpreadByCitation.py
python Calculate_Work_Following_Engage.py
python Calculate_Work_Distance_Engage_NoEngage_Pairwise.py
# ~2 CPU days
