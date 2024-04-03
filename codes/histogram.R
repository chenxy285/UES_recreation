# Read the data
df_pk <- read.csv("output/park_clean.csv")
df_ngs <- read.csv("output/ngs_clean.csv")
 
# Create a combined data frame
df_combined <- rbind(data.frame(value = df_ngs$total_dur, group = "Neighbourhood"),
                     data.frame(value = df_pk$total_dur, group = "Further away"))

ggplot(data=df_combined, aes(x=value, fill=group))+
  geom_histogram()+
  labs(x = "Total visit duration in the past year (min)", 
       y = "Frequency (no. of respondents)", 
       title = "Histogram of Total Visit Duration",
       fill = "Type of green space") +
  scale_fill_manual(values = c("Neighbourhood" = "pink",
                               "Further away" = "lightblue")) +  # Change legend labels
  theme_light()+
  theme(text = element_text(size = 14))


