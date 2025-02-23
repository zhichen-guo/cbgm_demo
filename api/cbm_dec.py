import torch
from torch import nn
from torch.nn import functional as F
from typing import Type
import numpy as np
from torch.autograd import Variable
import matplotlib
import matplotlib.pyplot as plt
import io

matplotlib.use('AGG')

class Generator_Simple(nn.Module):
    def __init__(self, latent_dim: int ,num_channels: int):
        super().__init__()
        self.latent_dim = latent_dim
        self.h1_dim = 1024
        self.fc1 = nn.Sequential(
            nn.Linear(self.latent_dim, self.h1_dim),
            nn.BatchNorm1d(self.h1_dim),
            nn.ReLU(inplace=True)
        )
        self.h2_nchan = 128
        h2_dim = 7 * 7 * self.h2_nchan
        self.fc2 = nn.Sequential(
            nn.Linear(self.h1_dim, h2_dim),
            nn.BatchNorm1d(h2_dim),
            nn.ReLU(inplace=True)
        )
        self.h3_nchan = 64
        self.conv1 = nn.Sequential(
            # nn.Upsample(scale_factor=2, mode='nearest'),
            # nn.Conv2d(self.h2_nchan, self.h3_nchan,
            #           kernel_size=5, stride=1, padding=2),
            nn.ConvTranspose2d(self.h2_nchan, self.h3_nchan,
                               kernel_size=4, stride=2, padding=1),
            nn.BatchNorm2d(self.h3_nchan),
            nn.ReLU(inplace=True)
        )
        self.conv2 = nn.Sequential(
            # nn.Upsample(scale_factor=2, mode='nearest'),
            # nn.Conv2d(self.h3_nchan, 1,
            #           kernel_size=5, stride=1, padding=2),
            nn.ConvTranspose2d(self.h3_nchan, num_channels, kernel_size=4, stride=2, padding=1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.fc1(x.squeeze())
        x = self.fc2(x).view(-1, self.h2_nchan, 7, 7)
        x = self.conv1(x)
        x = self.conv2(x)
        return x

class CBM_plus_Dec(nn.Module):
    def __init__(self,n_concepts,concept_bins,emb_size,noise_dim,concept_type,num_channels,gen_type="simple"):
        super().__init__()
        self.n_concepts=n_concepts

        self.emb_size=emb_size
        self.noise_dim=noise_dim
        self.concept_type=concept_type
        self.concept_bins=concept_bins
        self.num_channels=num_channels
        self.gen_type=gen_type
        self._build_model_()
    
    def _build_model_(self):
        self.concept_prob_generators = torch.nn.ModuleList()
        self.concept_context_generators = torch.nn.ModuleList()
        self.sigmoid = torch.nn.Sigmoid()
        for c in range(self.n_concepts):

            self.concept_context_generators.append(
                torch.nn.Sequential(*[
                    torch.nn.Linear(self.noise_dim,
                            self.concept_bins[c] * self.emb_size),
                        nn.BatchNorm1d(self.concept_bins[c] * self.emb_size)
                        ]))

            self.concept_prob_generators.append(
                torch.nn.Sequential(*[torch.nn.Linear(self.concept_bins[c]* self.emb_size,
                        self.concept_bins[c])
                     ]))


        self.concept_context_generators.append(
        torch.nn.Sequential(*[
            torch.nn.Linear(self.noise_dim,self.emb_size),
                nn.BatchNorm1d(self.emb_size)
                ]))

        self.g_latent=self.emb_size*(self.n_concepts+1)
        self.g_latent+=sum(self.concept_bins)

        if(self.gen_type=="simple"):
            self.gen = Generator_Simple(self.g_latent,self.num_channels)
        else:
            self.gen = Generator(self.g_latent,self.num_channels)
            self.gen.weight_init(mean=0.0, std=0.02)


    def forward(self,h,probs=None,return_all=False):
        non_concept_latent=None
        all_concept_latent=None
        all_concepts=None
        all_logits=None
        for c in range(self.n_concepts+1):
            ### 1 generate context
            context= self.concept_context_generators[c](h)
            if c <self.n_concepts :
                ### 2 get prob given concept
                if(probs==None):
                    logits =  self.concept_prob_generators[c](context)
                    prob_gumbel = F.softmax(logits, dim=1)
                else:
                    logits=probs[c]
                    prob_gumbel=probs[c]
                for i in range(self.concept_bins[c]):
                    temp_concept_latent =  context[:, (i*self.emb_size):((i+1)*self.emb_size)] * prob_gumbel[:,i].unsqueeze(-1)
                    if i==0:
                        concept_latent = temp_concept_latent
                    else:
                        concept_latent = concept_latent+ temp_concept_latent

                if all_concept_latent== None:
                    all_concept_latent=concept_latent
                else:
                    all_concept_latent= torch.cat((all_concept_latent,concept_latent),1)

                if all_concepts == None:
                    all_concepts=prob_gumbel
                    all_logits=logits
                else:
                    all_concepts=torch.cat((all_concepts,prob_gumbel),1)
                    all_logits=torch.cat((all_logits,logits),1)

            else:
                if non_concept_latent== None:
                    non_concept_latent= context
                else:
                    non_concept_latent= torch.cat((non_concept_latent,context),1)


        latent=torch.cat((all_concepts,all_concept_latent,non_concept_latent),1).unsqueeze(-1).unsqueeze(-1)

        fake_data = self.gen(latent)
        if(return_all):
            return fake_data,all_logits,all_concept_latent,non_concept_latent
        else:
            return fake_data

def create_cb_dec():
    config_cb_vaegan_mnist = {
        'dataset': {
            'name': 'color_mnist',
            'img_size': 28,
            'batch_size': 64,
            'test_batch_size': 1000,
            'num_channels': 3,
        },
        'model': {
            'type': 'cb_vaegan',
            'latent_noise_dim': 64,
            'input_latent_dim': 10,
            'pre_concept_latent_dim': 124,
            'pre_concept_layers': 5,
            'has_concepts': True,
            'concepts': {
                'emb_size': 16,
                'concept_names': ["label", "red", "green"],
                'types': ["cat", "bin", "bin"],
                'concept_latent': [10, 10, 10],
                'concept_hidden': [124, 124, 124],
                'concept_bins': [10, 2, 2],
                'concept_output': [10, 1, 1],
            },
        }
    }

    concepts = config_cb_vaegan_mnist["model"]["concepts"]
    n_concepts = len(concepts["concept_names"])
    concept_bins = concepts["concept_bins"]
    emb_size = concepts["emb_size"]
    noise_dim = config_cb_vaegan_mnist["model"]["latent_noise_dim"]
    concept_type = concepts["types"]
    num_channels = config_cb_vaegan_mnist["dataset"]["num_channels"]

    color_mnist_cb_dec = CBM_plus_Dec(n_concepts, concept_bins, emb_size, noise_dim, concept_type, num_channels, "simple")

    color_mnist_cb_dec.load_state_dict(torch.load('./trained_models/cb_vaegan_color_mnist.pt', map_location=torch.device('cpu'), weights_only=True))  # Make sure the path is correct

    return color_mnist_cb_dec

def generate_samples():
    color_mnist_cb_dec = create_cb_dec()
    color_mnist_cb_dec.eval()

    # Step 3: Generate random latent vectors z from N(0, I)
    latent_dim = 64  # Use the same latent dimensionality as your model
    batch_size = 10  # Number of images you want to generate
    z = torch.randn(batch_size, latent_dim)  # Sample from a standard normal distribution

    # Step 4: Pass the latent vectors through the decoder to generate images
    with torch.no_grad():  # Disable gradient calculation for inference
        generated_images = color_mnist_cb_dec(z)
        #generated_images, all_logits, all_concept_latent, non_concept_latent = color_mnist_cb_dec(z, return_all=True)
        #print(all_logits)
        #print(F.softmax(all_logits))

    # Step 5: Visualize the generated images (optional)
    def show_images(images):
        fig, axes = plt.subplots(1, len(images), figsize=(len(images), 2))
        for i, img in enumerate(images):
            img = img.permute(1, 2, 0)  # Rearrange dimensions to HWC for plotting
            axes[i].imshow(img.cpu().numpy())
            axes[i].axis('off')
        #plt.show()
        plt.savefig('./generated_images/gens.png')
        plt.close(fig)

    show_images(generated_images)

def generate_steered_image(number, color):
    color_mnist_cb_dec = create_cb_dec()
    color_mnist_cb_dec.eval()

    z = torch.randn(10, 64)
    number_prob = [1.0e-10 for i in range(10)]
    number_prob[number] = 0.9999999991
    color_prob_red = [0.9, 0.1] if color == "red" else [0.1, 0.9]
    color_prob_green = [0.9, 0.1] if color == "green" else [0.1, 0.9]

    probs = [
        torch.tensor([number_prob for i in range(10)]), 
        torch.tensor([color_prob_red for i in range(10)]),
        torch.tensor([color_prob_green for i in range(10)])
    ]

    with torch.no_grad():
        generated_images = color_mnist_cb_dec(z, probs=probs)

    fig, axes = plt.subplots(1, len(generated_images), figsize=(len(generated_images), 2))
    for i, img in enumerate(generated_images):
        img = img.permute(1, 2, 0)  # Rearrange dimensions to HWC for plotting
        axes[i].imshow(img.cpu().numpy())
        axes[i].axis('off')

    image_buf = io.BytesIO()
    plt.savefig(image_buf, format="png")
    plt.close(fig)
    return image_buf

def generate_interpretable_image():
    color_mnist_cb_dec = create_cb_dec()
    color_mnist_cb_dec.eval()

    z = torch.randn(10, 64)
    
    with torch.no_grad():
        generated_images, all_logits, all_concept_latent, non_concept_latent = color_mnist_cb_dec(z, return_all=True)
        probs = F.softmax(all_logits, dim=1)
    
    fig, axes = plt.subplots(1, len(generated_images), figsize=(len(generated_images), 2))
    for i, img in enumerate(generated_images):
        img = img.permute(1, 2, 0)  # Rearrange dimensions to HWC for plotting
        axes[i].imshow(img.cpu().numpy())
        axes[i].axis('off')

    image_buf = io.BytesIO()
    plt.savefig(image_buf, format="png")
    plt.close(fig)
    return [image_buf, probs]