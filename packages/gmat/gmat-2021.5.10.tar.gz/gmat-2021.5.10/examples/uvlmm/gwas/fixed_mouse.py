import logging
from gmat.gmatrix import agmat
from gmat.uvlmm.gwas import fixed
logging.basicConfig(level=logging.INFO)
pheno_file = 'pheno'
bed_file = 'plink'
# id-id-value form
agmat_file = 'test'
#agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='mat')
agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='id_id_val')

"""
fixed(pheno_file, bed_file, agmat_file, class_lst=["mean", "sex", "treat"], fix="mean + sex + treat", 
out_file='res.txt', condition_snp=None, npart=1, maxiter0=100, maxiter1=10,
          speed=True, pcut=1)
"""

fixed(pheno_file, bed_file, agmat_file, class_lst=None, fix=None, out_file='res.txt', condition_snp=None)

fixed(pheno_file, bed_file, agmat_file, class_lst=None, fix=None, out_file='res.txt', condition_snp=["gnf01.037.906", "mCV23431007"])

