import torch

def main():
    f = torch.tensor([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]])
    newF = torch.flatten(f)
    print(newF)

if __name__ == '__main__':
    main()