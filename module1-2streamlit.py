import streamlit as st
from Bio import Blast

#Blast.tool
#'biopython'

Blast.email = 'mpearc11@jhu.edu'

uploaded_file = st.file_uploader("Target FASTA File", type='fasta')
if st.button('run blast'):
    st.write('blast running...')
    target_nt_fasta = uploaded_file.read()
    result_stream = Blast.qblast('blastn', 'nt', target_nt_fasta)
    st.write('blast finished!')

if uploaded_file:
    with open('myblast.xml', 'wb') as out_stream:
        out_stream.write(result_stream.read())
    result_stream.close()
    result_stream = open('myblast.xml', 'rb')
    blast_record = Blast.read(result_stream)

hit = blast_record[0]
alignment = hit[0]

@st.fragment()
def file_download():
    st.download_button(
        label="Download Alignment",
        data=str(alignment),
        file_name='alignment.txt')
file_download()

st.code(hit)

num = 1

for i in blast_record[:10]:
    st.write("HIT" + str(num))
    st.write(i[0])
    num = num +1
