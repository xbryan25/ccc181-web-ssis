<script setup lang="ts">
import type { FormError, FormSubmitEvent } from "@nuxt/ui";

interface CollegeFormState {
  collegeCode: string;
  collegeName: string;
}

const state = reactive({
  collegeCode: "",
  collegeName: "",
});

const collegeCodeRegex = /^[A-Z-]+$/;
const collegeNameRegex = /^[A-Za-z- ]+$/;

const validate = (state: CollegeFormState): FormError[] => {
  const errors = [];
  if (!state.collegeCode) {
    errors.push({ name: "collegeCode", message: "Required." });
  } else if (state.collegeCode && !collegeCodeRegex.test(state.collegeCode)) {
    errors.push({
      name: "collegeCode",
      message: "Uppercase letters & dashes only.",
    });
  }

  if (!state.collegeName) {
    errors.push({ name: "collegeName", message: "Required." });
  } else if (state.collegeName && !collegeNameRegex.test(state.collegeName)) {
    errors.push({
      name: "collegeName",
      message: "Letters, spaces, and dashes only.",
    });
  }

  return errors;
};

const toast = useToast();
async function onSubmit(event: FormSubmitEvent<typeof state>) {
  toast.add({
    title: "Success",
    description: "The form has been submitted.",
    color: "success",
  });
  console.log(event.data);
}
</script>

<template>
  <UForm
    :validate="validate"
    :state="state"
    class="flex flex-col space-y-4"
    @submit="onSubmit"
  >
    <UFormField label="College Code" name="collegeCode" class="flex-1">
      <UInput v-model="state.collegeCode" class="w-full" />
    </UFormField>

    <UFormField label="College Name" name="collegeName" class="flex-1">
      <UInput v-model="state.collegeName" class="w-full" />
    </UFormField>
  </UForm>
</template>
