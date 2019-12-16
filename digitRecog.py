import numpy as np
import cv2 as cv

def load_base(fn):
    a = np.loadtxt(fn, np.float32, delimiter=',')
    samples, responses = a[:,1:], a[:,0]
    return samples, responses

class DigitModel(object):
    class_n = 26
    train_ratio = 0.5

    def load(self, fn):
        self.model.load(fn)
    def save(self, fn):
        self.model.save(fn)

    def unroll_samples(self, samples):
        sample_n, var_n = samples.shape
        new_samples = np.zeros((sample_n * self.class_n, var_n+1), np.float32)
        new_samples[:,:-1] = np.repeat(samples, self.class_n, axis=0)
        new_samples[:,-1] = np.tile(np.arange(self.class_n), sample_n)
        return new_samples

    def unroll_responses(self, responses):
        sample_n = len(responses)
        new_responses = np.zeros(sample_n*self.class_n, np.int32)
        resp_idx = np.int32( responses + np.arange(sample_n)*self.class_n )
        new_responses[resp_idx] = 1
        return new_responses

class SVM(DigitModel):
    def __init__(self):
        self.model = cv.ml.SVM_create()

    def train(self, samples, responses):
        self.model.setType(cv.ml.SVM_C_SVC)
        self.model.setC(1)
        self.model.setKernel(cv.ml.SVM_RBF)
        self.model.setGamma(.1)
        self.model.train(samples, cv.ml.ROW_SAMPLE, responses.astype(int))

    def predict(self, samples):
        _ret, resp = self.model.predict(samples)
        return resp.ravel()

def recogBoard(board):
    model = SVM()
    samples, responses = load_base('./digits.data')
    model.train(samples, responses)
    verify = np.float32(board)
    result = model.predict(verify)
    return result