<template>
  <div class="form-container">
    <form @submit.prevent="submitForm">
      <input type="file" @change="previewImage1" accept="image/*" />
      <input type="file" @change="previewImage2" accept="image/*" />
      <button type="submit">Upload Images</button>
    </form>
    <div v-if="imageUrl" class="preview">
      <img :src="imageUrl" alt="First Image preview" />
    </div>
    <div v-if="imageUrl2" class="preview">
      <img :src="imageUrl2" alt="Second Image preview" />
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      image: null,
      imageUrl: null,
      image2: null,
      imageUrl2: null,
    };
  },
  methods: {
    previewImage1(event) {
      this.image = event.target.files[0];
      this.imageUrl = URL.createObjectURL(this.image);
    },
    previewImage2(event) {
      this.image2 = event.target.files[0];
      this.imageUrl2 = URL.createObjectURL(this.image2);
    },
    async submitForm() {
      const formData = new FormData();
      formData.append('image1', this.image);
      formData.append('image2', this.image2);

      try {
        const response = await axios.post('http://localhost:5000/upload-images', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        alert(response.data.message);
      } catch (error) {
        console.error('Error uploading images:', error);
        alert('Failed to upload images.');
      }
    },
  },
};
</script>

<style scoped>
.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

form {
  margin-bottom: 20px;
}

.preview img {
  max-width: 300px;
  max-height: 300px;
  margin-top: 20px;
}
</style>