import { Octokit } from '@octokit/rest';

const octokit = new Octokit();
const res = await octokit.rest.emojis.get();
const emojis = res.data;

export const options = {
  emojis,
  renderer: (token) => `<img alt="${token.name}" src="${token.emoji}" class="marked-emoji-img">`,
};
