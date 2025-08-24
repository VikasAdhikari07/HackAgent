import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import Header from "@/components/Header";
import { ArrowRight, ArrowLeft, CheckCircle, Sparkles, RefreshCw } from "lucide-react";
import { useNavigate } from "react-router-dom";

const categories = [
  { id: "marketing", name: "Marketing", description: "Brand awareness, campaigns, content marketing" },
  { id: "sales", name: "Sales", description: "Lead generation, conversion optimization, sales funnels" },
  { id: "seo", name: "SEO", description: "Search optimization, keyword strategy, content ranking" },
  { id: "content", name: "Content", description: "Content creation, editorial calendars, storytelling" },
  { id: "product", name: "Product", description: "Product development, features, user experience" },
  { id: "custom", name: "Custom", description: "Define your own strategy category" },
];

const enhancementTags = [
  "Add creativity",
  "Make concise", 
  "SEO optimized",
  "Marketing tone",
  "Professional style",
  "Customer-centric",
  "Growth-focused",
  "Short-form",
  "Detailed",
  "Experimental",
];

export default function Dashboard() {
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [prompt, setPrompt] = useState("");
  const [selectedEnhancements, setSelectedEnhancements] = useState<string[]>([]);
  const navigate = useNavigate();

  const handleCategorySelect = (categoryId: string) => {
    setSelectedCategory(categoryId);
  };

  const handleEnhancementToggle = (enhancement: string) => {
    setSelectedEnhancements(prev =>
      prev.includes(enhancement)
        ? prev.filter(e => e !== enhancement)
        : [...prev, enhancement]
    );
  };

  const handleNext = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleEnhancePrompt = () => {
    // This would call AI to enhance the prompt with selected enhancements
    alert("Prompt enhanced! This would integrate with AI API.");
  };

  const handleRegeneratePrompt = () => {
    // This would call AI to regenerate the prompt
    alert("Prompt regenerated! This would integrate with AI API.");
  };

  const handleGeneratePlan = () => {
    // Navigate to plan view page
    navigate("/plan");
  };

  const progressPercentage = (currentStep / 3) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      <Header />
      
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Progress Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-3xl font-bold text-gray-900">Strategy Builder</h1>
            <div className="text-sm text-gray-600">
              Step {currentStep} of 3
            </div>
          </div>
          <Progress value={progressPercentage} className="h-2" />
          <div className="flex justify-between mt-2 text-sm text-gray-500">
            <span>Select Category</span>
            <span>Enter Prompt</span>
            <span>Enhance & Generate</span>
          </div>
        </div>

        {/* Step 1: Select Category */}
        {currentStep === 1 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="bg-purple-100 text-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">1</span>
                Select Category
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                {categories.map((category) => (
                  <div
                    key={category.id}
                    className={`p-4 border-2 rounded-lg cursor-pointer transition-all hover:shadow-md ${
                      selectedCategory === category.id
                        ? "border-purple-500 bg-purple-50"
                        : "border-gray-200 hover:border-purple-300"
                    }`}
                    onClick={() => handleCategorySelect(category.id)}
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-semibold text-gray-900">{category.name}</h3>
                        <p className="text-sm text-gray-600 mt-1">{category.description}</p>
                      </div>
                      {selectedCategory === category.id && (
                        <CheckCircle className="h-5 w-5 text-purple-500 flex-shrink-0" />
                      )}
                    </div>
                  </div>
                ))}
              </div>
              <div className="flex justify-end pt-4">
                <Button
                  onClick={handleNext}
                  disabled={!selectedCategory}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                >
                  Next Step
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 2: Enter Prompt */}
        {currentStep === 2 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="bg-purple-100 text-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">2</span>
                Enter Prompt
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="prompt">Describe your idea or goal</Label>
                <Textarea
                  id="prompt"
                  placeholder="Describe your idea or goal here..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="min-h-[120px] resize-none"
                />
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <span className="font-medium">Category:</span>
                <Badge variant="secondary">
                  {categories.find(c => c.id === selectedCategory)?.name}
                </Badge>
              </div>
              <div className="flex justify-between pt-4">
                <Button variant="outline" onClick={handleBack}>
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back
                </Button>
                <Button
                  onClick={handleNext}
                  disabled={!prompt.trim()}
                  className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                >
                  Next Step
                  <ArrowRight className="h-4 w-4 ml-2" />
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Step 3: Enhance Prompt Options */}
        {currentStep === 3 && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <span className="bg-purple-100 text-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold">3</span>
                Enhance & Generate
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Current Prompt Display */}
              <div className="space-y-2">
                <Label>Your Prompt</Label>
                <div className="p-3 bg-gray-50 rounded-lg border">
                  <p className="text-gray-700">{prompt}</p>
                </div>
              </div>

              {/* Enhancement Options */}
              <div className="space-y-3">
                <Label>Enhancement Options</Label>
                <div className="flex flex-wrap gap-2">
                  {enhancementTags.map((tag) => (
                    <Badge
                      key={tag}
                      variant={selectedEnhancements.includes(tag) ? "default" : "outline"}
                      className={`cursor-pointer transition-colors ${
                        selectedEnhancements.includes(tag)
                          ? "bg-purple-600 hover:bg-purple-700"
                          : "hover:bg-purple-50 hover:border-purple-300"
                      }`}
                      onClick={() => handleEnhancementToggle(tag)}
                    >
                      {tag}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="space-y-3">
                <div className="flex gap-3">
                  <Button
                    variant="outline"
                    onClick={handleEnhancePrompt}
                    className="flex-1"
                    disabled={selectedEnhancements.length === 0}
                  >
                    <Sparkles className="h-4 w-4 mr-2" />
                    Enhance Prompt
                  </Button>
                  <Button
                    variant="outline"
                    onClick={handleRegeneratePrompt}
                    className="flex-1"
                  >
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Regenerate Prompt
                  </Button>
                </div>
                
                <div className="flex justify-between pt-4">
                  <Button variant="outline" onClick={handleBack}>
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Back
                  </Button>
                  <Button
                    onClick={handleGeneratePlan}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700"
                  >
                    Generate Plan
                    <ArrowRight className="h-4 w-4 ml-2" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
