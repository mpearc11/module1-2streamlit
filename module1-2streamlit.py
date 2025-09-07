import streamlit as st
from Bio import Blast

#Blast.tool
#'biopython'

st.title('Automated Python Search App – Nucleotide BLAST')

#Blast.email = st.text_input('provide your jhu email')

st.header('Submit Query for BLASTn – Nucleotide Search')

uploaded_file = st.file_uploader("",type='fasta')

if uploaded_file is not None:
    st.success("FASTA file uploaded")
else:
    st.info("Please upload your target FASTA file")

if st.button('run blast'):
    target_nt_fasta = uploaded_file.read()
    with st.empty():
        st.write('blast running...')
        result_stream = Blast.qblast('blastn', 'nt', target_nt_fasta)
        st.write('blast finished!')

    with open('myblast.xml', 'wb') as out_stream:
        out_stream.write(result_stream.read())
    result_stream.close()
    result_stream = open('myblast.xml', 'rb')
    blast_record = Blast.read(result_stream)

    hit = blast_record[0]
    alignment = hit[0]
    
    @st.fragment()
    def alignment_download():
        st.download_button(
            label="Download Alignment",
            data=str(alignment),
            file_name='alignment.txt')
    alignment_download()
    
    st.code(hit)
    st.code('targets = ' + hit.targets)
    st.code('accession number = ' + hit.targets[0].name)
    
    num = 1
    
    for i in blast_record[:10]:
        st.write("HIT" + str(num))
        st.write(i[0])
        with open("top10hits.txt", "a") as f:
            f.write("HIT" + str(num) + "\n")
        with open("top10hits.txt", "a") as f:
            f.write(str(i[0]))
        num = num +1

    @st.fragment()
    def hit_download():
        with open('top10hits.txt') as f:
            st.download_button('Download Top 10 Hits', f)
    hit_download()
