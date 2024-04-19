import torch
import torch.nn as nn
import math


class CustomLSTM(nn.Module):
    def __init__(self, input_sz: int, hidden_sz: int):
        super().__init__()
        self.input_size = input_sz
        self.hidden_size = hidden_sz
        self.U_f = nn.Parameter(torch.Tensor(input_sz, hidden_sz))
        self.W_f = nn.Parameter(torch.Tensor(hidden_sz, hidden_sz))
        self.b_f = nn.Parameter(torch.Tensor(hidden_sz))
        self.U_i = nn.Parameter(torch.Tensor(input_sz, hidden_sz))
        self.W_i = nn.Parameter(torch.Tensor(hidden_sz, hidden_sz))
        self.b_i = nn.Parameter(torch.Tensor(hidden_sz))
        self.U_o = nn.Parameter(torch.Tensor(input_sz, hidden_sz))
        self.W_o = nn.Parameter(torch.Tensor(hidden_sz, hidden_sz))
        self.b_o = nn.Parameter(torch.Tensor(hidden_sz))
        self.U_g = nn.Parameter(torch.Tensor(input_sz, hidden_sz))
        self.W_g = nn.Parameter(torch.Tensor(hidden_sz, hidden_sz))
        self.b_g = nn.Parameter(torch.Tensor(hidden_sz))


        self.init_weights()

    def init_weights(self):
        stdv = 1.0 / math.sqrt(self.hidden_size)
        for weight in self.parameters():
            weight.data.uniform_(-stdv, stdv)

    def forward(self, x):

        bs, seq_sz, _ = x.shape
        hidden_seq = []
        carry_seq = []
        c_t = torch.zeros(bs, self.hidden_size)
        h_t = torch.zeros(bs, self.hidden_size)



        for t in range(seq_sz):
            x_t = x[:, t, :]
            f_t = torch.sigmoid(x_t @ self.U_f + h_t @ self.W_f + self.b_f)
            i_t = torch.sigmoid(x_t @ self.U_i + h_t @ self.W_i + self.b_i)
            o_t = torch.sigmoid(x_t @ self.U_o + h_t @ self.W_o + self.b_o)
            g_t = torch.tanh(x_t @ self.U_g + h_t @ self.W_g + self.b_g)
            c_t = f_t * c_t + i_t * g_t
            h_t = o_t * torch.tanh(c_t)
            hidden_seq.append(h_t.unsqueeze(1))
            carry_seq.append(c_t.unsqueeze(1))


        hidden_seq = torch.cat(hidden_seq,dim=1)
        carry_seq = torch.cat(carry_seq, dim=1)

        return h_t, hidden_seq, c_t, carry_seq
