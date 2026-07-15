import { defineStore } from "pinia";

export const NotificationStore = defineStore("NotificationStore", {
  state: () => {
    return {
      message_type: "",
      message: "",
      timerId: null,
    };
  },

  actions: {
    add_message(type, message) {
      if (this.timerId) {
        clearTimeout(this.timerId);
      }
      console.log("called");

      this.message_type = type;
      this.message = message;

      this.timerId = setTimeout(() => {
        this.message_type = "";
        this.message = "";
        this.timerId = null;
      }, 5000);
    },
  },
});
