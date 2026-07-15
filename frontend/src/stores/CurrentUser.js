import { defineStore } from "pinia";

export const CurrentUserStore = defineStore("user", {
  state: () => {
    const saved = localStorage.getItem("user_state");

    return saved
      ? JSON.parse(saved)
      : {
          user: null,
          role: null,
        };
  },

  actions: {
    login(user, role) {
      this.user = user;
      this.role = role;
    },

    logout() {
      this.user = null;
      this.role = null;
    },
  },

  persist: true,
});
