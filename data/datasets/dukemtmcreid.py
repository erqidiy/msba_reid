# encoding: utf-8
"""
@author:  liaoxingyu
@contact: liaoxingyu2@jd.com
"""

import glob
import os.path as osp
import re

from .dataset_loader import ImageDataset


class DukeMTMCreID(ImageDataset):
    """DukeMTMC-reID.

    Reference:
        - Ristani et al. Performance Measures and a Data Set for Multi-Target, Multi-Camera Tracking. ECCVW 2016.
        - Zheng et al. Unlabeled Samples Generated by GAN Improve the Person Re-identification Baseline in vitro. ICCV 2017.

    URL: `<https://github.com/layumi/DukeMTMC-reID_evaluation>`_

    Dataset statistics:
        - identities: 1404 (train + query).
        - images:16522 (train) + 2228 (query) + 17661 (gallery).
        - cameras: 8.
    """
    dataset_dir = 'DukeMTMC-reID'
    dataset_url = 'http://vision.cs.duke.edu/DukeMTMC/data/misc/DukeMTMC-reID.zip'

    def __init__(self, root='datasets', **kwargs):
        # self.root = osp.abspath(osp.expanduser(root))
        self.root = root
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        self.train_dir = osp.join(self.dataset_dir, 'bounding_box_train')
        self.query_dir = osp.join(self.dataset_dir, 'query')
        self.gallery_dir = osp.join(self.dataset_dir, 'bounding_box_test')

        required_files = [
            self.dataset_dir,
            self.train_dir,
            self.query_dir,
            self.gallery_dir
        ]
        self.check_before_run(required_files)

        train = self.process_dir(self.train_dir, relabel=True)
        query = self.process_dir(self.query_dir, relabel=False)
        gallery = self.process_dir(self.gallery_dir, relabel=False)

        super(DukeMTMCreID, self).__init__(train, query, gallery, **kwargs)

    def process_dir(self, dir_path, relabel=False):
        img_paths = glob.glob(osp.join(dir_path, '*.jpg'))
        pattern = re.compile(r'([-\d]+)_c(\d)')

        pid_container = set()
        for img_path in img_paths:
            pid, _ = map(int, pattern.search(img_path).groups())
            pid_container.add(pid)
        pid2label = {pid: label for label, pid in enumerate(pid_container)}

        data = []
        for img_path in img_paths:
            pid, camid = map(int, pattern.search(img_path).groups())
            assert 1 <= camid <= 8
            camid -= 1  # index starts from 0
            if relabel: pid = pid2label[pid]
            data.append((img_path, pid, camid))

        return data
