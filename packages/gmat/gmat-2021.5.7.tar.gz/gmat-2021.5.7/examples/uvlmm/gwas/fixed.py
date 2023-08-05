import logging
from gmat.gmatrix import agmat
from gmat.uvlmm.gwas import fixed, fixed_min
logging.basicConfig(level=logging.INFO)
pheno_file = 'pheno'
bed_file = 'plink'
# id-id-value form
agmat_file = 'test'
agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='id_id_val')
"""
fixed(pheno_file, bed_file, agmat_file, out_file='res5.txt', npart=1, maxiter0=100, maxiter1=10,
          speed=True, pcut=1.0e-2)
fixed(pheno_file, bed_file, agmat_file, out_file='res6.txt', npart=1, maxiter0=100, maxiter1=10,
          speed=False, pcut=1.0e-5)
#fixed_min(pheno_file, bed_file, agmat_file, out_file='res2.txt', npart=20)
"""


fixed(pheno_file, bed_file, agmat_file, class_lst=["mean", "sex", "treat"], fix="mean + sex + treat", 
out_file='res.txt', condition_snp=None, npart=1, maxiter0=100, maxiter1=10,
          speed=True, pcut=5.0e-1)
