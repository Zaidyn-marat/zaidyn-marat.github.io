import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const members = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/members' }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    bounty: z.string(),
    status: z.string().default('ACTIVE OR ALIVE'),
    avatar: z.string(),
    orcid: z.string().optional(),
    alumni: z.coerce.boolean().default(false), // 兼容 true 或 "true"
    destination: z.string().optional(),
    order: z.number().default(99),
  }),
});


const research = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/research' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    image: z.string().optional(),
    order: z.number().default(1),
  }),
});

const publications = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/publications' }),
  schema: z.object({
    title: z.string(),
    authors: z.string(),
    journal: z.string(),
    year: z.number(),
    doi: z.string().optional(),
  }),
});

const courses = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/courses' }),
  schema: z.object({
    code: z.string(),
    title: z.string(),
    semester: z.string(),
    instructor: z.string(),
  }),
});
const instrumentation = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/instrumentation' }),
  schema: z.object({
    name: z.string(),
    category: z.string(), // 例如 "Computing Cluster" 或 "Telescope / Hardware"
    specs: z.string(),    // 核心参数，如 "RTX 4070 Ti / 32GB RAM / Ubuntu"
    image: z.string().optional(),
  }),
});
const software = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/software' }),
  schema: z.object({
    name: z.string(),
    language: z.string(), // 例如 "Python / C++"
    summary: z.string(),
    repo: z.string(),     // GitHub 仓库链接
    paper: z.string().optional(), // 关联论文链接（可选）
  }),
});

const news = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/news' }),
  schema: z.object({
    date: z.coerce.date(), // 自动解析 YYYY-MM-DD
    title: z.string(),
  }),
});

export const collections = { 
  members, research, publications, courses, instrumentation, software, news 
};
