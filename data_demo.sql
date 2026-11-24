-- DATA DEMO untuk mengisi grafik dashboard
-- Jalankan di Supabase: SQL Editor -> New query -> paste -> Run
-- Semua user demo memakai password: admin123

insert into users (username, password_hash, nama, created_at) values
 ('budi',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Budi Santoso',   now() - interval '6 days'),
 ('siti',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Siti Rahma',     now() - interval '5 days'),
 ('andi',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Andi Pratama',   now() - interval '4 days'),
 ('dewi',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Dewi Lestari',   now() - interval '4 days'),
 ('rizky',  'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Rizky Hidayat',  now() - interval '2 days'),
 ('maya',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Maya Putri',     now() - interval '2 days'),
 ('fajar',  'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Fajar Nugroho',  now() - interval '2 days'),
 ('nina',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Nina Kartika',   now() - interval '1 days'),
 ('yoga',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Yoga Saputra',   now()),
 ('lina',   'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Lina Marlina',   now()),
 ('lama1',  'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Hendra Wijaya',  now() - interval '20 days'),
 ('lama2',  'scrypt:32768:8:1$nimpqzuuSnxRDX6F$a382fa2bed5a9f45c0679b8970099afd09bdfafe06356332e620b115289fa4cb07d076f960087acec34a25e762ed15ea6c9f7a0b4a8ba58dbaf77c006a83bc4e', 'Agus Salim',     now() - interval '30 days')
on conflict (username) do nothing;
