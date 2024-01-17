<template>

<div class="row">
  <div class="col-3"></div>
  <div class="col-3">  

    <div class="form-container">
    <form @submit.prevent="submitForm">
      <input type="file" @change="previewImage" accept="image/*" />
      <button type="submit">Upload Image</button>
    </form>
    <div v-if="imageUrl" class="preview">
      <img :src="imageUrl" alt="Image preview" />
    </div>
  </div>

    </div>


  <div class="col-3"></div>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      image: null,
      imageUrl: null,
    };
  },
  methods: {
    previewImage(event) {
      this.image = event.target.files[0];
      this.imageUrl = URL.createObjectURL(this.image);
    },
    async submitForm() {
      const formData = new FormData();
      formData.append('image', this.image);

      try {
        const response = await axios.post('http://localhost:5000/test', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        alert(response.data.message);
      } catch (error) {
        console.error('Error uploading image:', error);
        alert('Failed to upload image.');
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